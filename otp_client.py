"""Клиент Online Test Pad: вход и навигация по папкам/тестам.

Работает через Playwright: рендерит страницы как в обычном браузере,
поэтому не зависит от внутренних AJAX-API сайта.

Безопасность: логин и пароль живут только в памяти процесса и не логируются.
Авторизационная сессия (cookies) сохраняется в data/otp_state.json, чтобы
кабинет оставался подключённым после перезапуска сервера; пароль в файл
никогда не пишется.
"""

import json
import os
import queue
import re
import threading
from playwright.sync_api import sync_playwright

BASE = "https://app.onlinetestpad.com"
LOGIN_URL = "https://onlinetestpad.com/ru/account/login"
TESTS_URL = BASE + "/tests"
STATE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "otp_state.json"
)


class OTPError(Exception):
    """Ошибка работы с Online Test Pad."""


class OTPClient:
    """Тонкая обёртка над браузерной сессией Online Test Pad."""

    def __init__(self):
        self._pw = None
        self._browser = None
        self._context = None
        self._page = None
        self.email = None
        self._account_tests_cache = None
        self._lock = threading.RLock()
        self._q = queue.Queue()
        self._thread = None

    # ---------------------------------------------------------------
    # Выполнение Playwright-кода в отдельном worker-потоке.
    # В потоке Flask (main) может быть запущен asyncio-loop (IDE/отладчик),
    # из-за чего sync-API Playwright падает; в worker-потоке его нет.
    # ---------------------------------------------------------------
    def _run(self, fn, *args, **kwargs):
        if threading.current_thread() is self._thread:
            return fn(*args, **kwargs)
        self._ensure_worker()
        evt = threading.Event()
        box = {}

        def runner():
            try:
                box["v"] = fn(*args, **kwargs)
            except BaseException as e:  # noqa: BLE001 — пробрасываем всё на вызывающую сторону
                box["e"] = e
            finally:
                evt.set()

        self._q.put(runner)
        evt.wait()
        if "e" in box:
            raise box["e"]
        return box["v"]

    def _ensure_worker(self):
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(
                target=self._worker_loop, name="otp-playwright", daemon=True
            )
            self._thread.start()

    def _worker_loop(self):
        while True:
            task = self._q.get()
            if task is None:
                break
            task()

    def stop_worker(self):
        self._q.put(None)

    # ---------------------------------------------------------------
    # Управление браузером
    # ---------------------------------------------------------------
    def _start(self):
        return self._run(self._impl_start)

    def _impl_start(self):
        if self._page is not None:
            return
        with self._lock:
            self._pw = sync_playwright().start()
            # без --no-sandbox: Playwright добавляет его при запуске от администратора,
            # из-за чего Chromium печатает предупреждение в консоль сервера.
            self._browser = self._pw.chromium.launch(
                headless=True,
                ignore_default_args=["--no-sandbox"],
            )
            state = self._load_state()
            if state:
                self._context = self._browser.new_context(
                    storage_state=state,
                    locale="ru-RU",
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
                    ),
                )
                self.email = self._stored_email
            else:
                self._context = self._browser.new_context(
                    locale="ru-RU",
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
                    ),
                )
            self._page = self._context.new_page()

    def _load_state(self):
        """Восстанавливает сохранённую сессию (cookies) из файла."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._stored_email = data.get("email")
            return {"cookies": data.get("cookies", []), "origins": data.get("origins", [])}
        except Exception:
            self._stored_email = None
            return None

    def _save_state(self):
        """Сохраняет текущую сессию (cookies + email) в файл."""
        try:
            state = self._context.storage_state()
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump({"email": self.email, **state}, f, ensure_ascii=False)
        except Exception:
            pass

    def _clear_state(self):
        """Удаляет сохранённую сессию (выход/истечение)."""
        self.email = None
        try:
            if os.path.exists(STATE_FILE):
                os.remove(STATE_FILE)
        except Exception:
            pass

    def close(self):
        return self._run(self._impl_close)

    def _impl_close(self):
        # НЕ очищаем сохранённую сессию: сервер может перезапускаться,
        # а явный выход (logout) сам вызывает _clear_state()
        try:
            if self._browser:
                self._browser.close()
        finally:
            self._pw = self._browser = self._context = self._page = None
            self.email = None

    @property
    def connected(self):
        # поднимаем браузер, если ещё нет — так статус учитывает
        # восстановленную с диска сессию после перезапуска сервера
        if self._page is None:
            self._run(self._impl_start)
        return self._page is not None and self.email is not None

    # ---------------------------------------------------------------
    # Вход
    # ---------------------------------------------------------------
    def login(self, email, password):
        return self._run(self._impl_login, email, password)

    def _impl_login(self, email, password):
        with self._lock:
            self._start()
            page = self._page

            # уже вошли ранее (форма входа не показывается) — просто сохраняем сессию
            page.goto(LOGIN_URL + "?ReturnUrl=/tests",
                      wait_until="domcontentloaded", timeout=30000)
            if not page.locator("#txtEmail").count() and self._is_authenticated(page):
                self.email = email
                self._save_state()
                return {"email": email}

            # заполняем форму (с диагностикой, если поле не появилось)
            email_field = page.locator("#txtEmail")
            try:
                email_field.wait_for(state="visible", timeout=30000)
            except Exception:
                self._dump_login_state("txtEmail not found")
                # fallback: любое поле с type=email
                alt = page.locator('input[type="email"]')
                if alt.count():
                    alt.first.fill(email)
                else:
                    raise OTPError(
                        f"Не найдено поле e-mail на странице входа. "
                        f"Текущий URL: {page.url}"
                    )
            else:
                email_field.fill(email)

            pass_field = page.locator("#txtPassword")
            if pass_field.count() == 0:
                alt = page.locator('input[type="password"]')
                if alt.count():
                    alt.first.fill(password)
                else:
                    raise OTPError("Не найдено поле пароля на странице входа.")
            else:
                pass_field.fill(password)

            submit = (
                page.locator('button[type="submit"]')
                .or_(page.locator('button:has-text("Войти")'))
                .or_(page.locator('input[type="submit"]'))
            )
            submit.first.click()

            # ждём перехода в кабинет (URL после входа может быть любым,
            # поэтому успех определяем по появлению меню пользователя)
            ok = False
            for _ in range(40):  # до 20 с
                page.wait_for_timeout(500)
                if self._is_authenticated(page):
                    ok = True
                    break
                if not page.locator("#txtEmail").count():
                    if self._is_authenticated(page):
                        ok = True
                        break
            if ok:
                self.email = email
                self._save_state()
                return {"email": email}

            self._dump_auth_state()
            raise OTPError("Не удалось войти. Проверьте логин/пароль или капчу на сайте.")

    @staticmethod
    def _is_authenticated(page):
        """Признак того, что открыт личный кабинет (а не страница входа)."""
        if page.locator('a[href*="logout"], a[href*="logout?"]').count():
            return True
        if page.locator('a[href*="/profile"]').count():
            return True
        return False

    def _dump_login_state(self, tag):
        """Диагностика: что на странице входа, если не нашли поле e-mail."""
        try:
            page = self._page
            info = {"tag": tag, "url": page.url, "title": page.title()}
            info["body"] = page.inner_text("body")[:400].replace("\n", " | ")
            info["inputs"] = page.evaluate(
                "() => [...document.querySelectorAll('input')].map(i => "
                "({id:i.id, type:i.type, name:i.name, cls:i.className}))"
            )
            self._last_dump = info
            print(f"[otp] {tag} url={info['url']}", flush=True)
            print(f"[otp] inputs: {info['inputs']}", flush=True)
        except Exception:
            pass

    def _dump_auth_state(self):
        """Диагностика: сохраняем, что происходит на странице при сбое входа."""
        try:
            page = self._page
            err = ""
            for sel in (".alert, .error, .validation-summary-errors, .invalid-feedback, .text-danger"):
                for el in page.locator(sel).all():
                    txt = (el.inner_text() or "").strip()
                    if txt:
                        err += txt + "\n"
            self._last_dump = {"url": page.url, "title": page.title(), "errors": err}
            print(f"[otp] login fail url={page.url} errors={err[:500]!r}", flush=True)
        except Exception:
            pass

    # ---------------------------------------------------------------
    # Сбор папок и тестов
    # ---------------------------------------------------------------
    def fetch_disciplines(self):
        return self._run(self._impl_fetch_disciplines)

    def _impl_fetch_disciplines(self):
        """Возвращает список {name, tests:[{id, title, href}]}."""
        with self._lock:
            if not self.connected:
                raise OTPError("Нет активной сессии. Сначала войдите.")
            page = self._page
            page.goto(TESTS_URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2500)  # ждём ajax-загрузку

            data = page.evaluate(self._EXTRACT_JS)
            tests = data.get("tests", [])
            folders = data.get("folders", [])

            # группируем тесты по папке из разметки
            groups = {}
            for t in tests:
                fname = (t.get("folder") or "").strip() or "Без папки"
                groups.setdefault(fname, []).append(t)

            disciplines = [
                {"name": name, "tests": [self._to_test(t) for t in items]}
                for name, items in groups.items()
            ]

            # если папок из разметки не нашлось — кучно в одну дисциплину
            if len(disciplines) <= 1 and folders:
                disciplines = [{"name": name, "tests": []} for name in folders[:200]]
                for t in tests:
                    disciplines[0]["tests"].append(self._to_test(t))

            return disciplines or [], data

    @staticmethod
    def _to_test(t):
        return {"id": t.get("id"), "title": t.get("title"), "href": t.get("href")}

    # JS, извлекающий из личного кабинета ссылки на тесты и заголовки папок
    _EXTRACT_JS = """
        () => {
            const out = { tests: [], folders: [], samples: [] };
            const seen = new Set();
            for (const a of document.querySelectorAll('a[href]')) {
                const href = a.getAttribute('href') || '';
                const m = href.match(/(?:testview|test)\\/(\\d+)/);
                if (!m) continue;
                const text = (a.innerText || a.getAttribute('title') || a.getAttribute('aria-label') || '').trim();
                if (!text) continue;
                const key = m[1] + '|' + text;
                if (seen.has(key)) continue;
                seen.add(key);
                let folder = '';
                let el = a;
                for (let i = 0; i < 5 && el; i++) {
                    el = el.parentElement;
                    if (!el) break;
                    if (/folder|cat|group|list-group|card|panel|item/i.test(el.className || '')) {
                        const h = el.querySelector('h1,h2,h3,h4,h5,[class*=title],[class*=name]');
                        if (h) { folder = h.innerText.trim(); break; }
                    }
                }
                out.tests.push({ id: m[1], title: text, href: href, folder: folder });
            }
            for (const h of document.querySelectorAll('h1,h2,h3,h4,h5,[class*=folder],[class*=cat]')) {
                const t = (h.innerText || '').trim().replace(/\\s+/g, ' ');
                if (t && t.length < 80) out.folders.push(t);
            }
            // несколько примеров ссылок со страницы для диагностики
            for (const a of document.querySelectorAll('a[href]')) {
                const href = a.getAttribute('href') || '';
                const text = (a.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 80);
                if (!text) continue;
                out.samples.push({ text: text, href: href });
                if (out.samples.length >= 40) break;
            }
            return out;
        }
    """

    # ---------------------------------------------------------------
    # Обход теста и сбор вопросов
    # ---------------------------------------------------------------
    def fetch_test_questions(self, url):
        return self._run(self._impl_fetch_test_questions, url)

    def _impl_fetch_test_questions(self, url):
        """Проходит тест по ссылке и собирает все вопросы.

        Результат фиксируется только кнопкой «Завершить» — мы её НЕ нажимаем,
        поэтому завершённых прохождений не создаётся. При повторном обходе
        страница предлагает «Продолжить» незавершённую попытку — используем её,
        чтобы не плодить новые попытки.
        """
        with self._lock:
            self._start()
            page = self._context.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(1200)

                # cookie-баннер, если всплыл
                accept = page.locator('button:has-text("Принять")')
                if accept.count() and accept.first.is_visible():
                    accept.first.click()
                    page.wait_for_timeout(400)

                # стартовая страница (регистрация + количество вопросов)
                total = None
                if not page.locator(".otp-item-view-question").count():
                    total = self._read_count(page)
                    self._fill_regform(page)
                    # предпочитаем НОВЫЙ проход: так соберём все вопросы с начала.
                    # «Продолжить» используем только если новый проход недоступен.
                    if page.locator("input[name=btnNext]").count():
                        self._click_robust(page.locator("input[name=btnNext]").first)
                    elif page.locator("input[name=btnRestoreAttempt]").count():
                        self._click_robust(page.locator("input[name=btnRestoreAttempt]").first)
                    page.wait_for_timeout(1200)

                if not page.locator(".otp-item-view-question").count():
                    raise OTPError("Не удалось начать прохождение теста. "
                                   "Возможно, тест требует доступ или закрыт.")

                questions = []
                seen = set()
                for _ in range(200):
                    q = page.evaluate(self._QUESTION_JS)
                    if not q.get("qtext"):
                        break
                    key = (q.get("qid"), q.get("qtext")[:60])
                    if key in seen:
                        break
                    seen.add(key)
                    questions.append(q)

                    # если собрали все вопросы — НЕ жмём «Далее», чтобы не завершить тест
                    if total is not None and len(questions) >= total:
                        break
                    self._answer_first(page)
                    nxt = page.locator("input[name=btnNext]")
                    if nxt.count() and nxt.first.is_visible():
                        self._click_robust(nxt.first)
                        page.wait_for_timeout(700)
                    else:
                        break  # последний вопрос — «Завершить» не нажимаем

                return {
                    "title": page.title(),
                    "url": url,
                    "count": len(questions),
                    "total_known": total,
                    "questions": questions,
                }
            finally:
                page.close()

    @staticmethod
    def _click_robust(locator, timeout=8000):
        """Клик с запасными вариантами: обычный → force → через JS.

        Кнопки onlinetestpad иногда перекрываются контентом вопроса
        (pointer-events перехватывает другой элемент) — тогда обычный
        клик Playwright падает по таймауту.
        """
        try:
            locator.click(timeout=timeout)
            return
        except Exception:
            pass
        try:
            locator.click(force=True, timeout=timeout)
            return
        except Exception:
            pass
        locator.evaluate("el => el.click()")

    @staticmethod
    def _read_count(page):
        try:
            b = page.locator(".otp-item-view-itemscount b")
            if b.count():
                return int(b.first.inner_text())
        except Exception:
            pass
        return None

    @staticmethod
    def _fill_regform(page):
        """Заполняет поля формы регистрации теста."""
        for inp in page.locator(".otp-item-view-regform input").all():
            try:
                if not inp.is_visible():
                    continue
                t = (inp.get_attribute("type") or "text").lower()
                if t in ("text", "email", "tel", "number", "date", ""):
                    if t == "number":
                        inp.fill("1")
                    elif t == "date":
                        inp.fill("01.01.2000")
                    else:
                        inp.fill("Технический обход")
            except Exception:
                continue

    @staticmethod
    def _answer_first(page):
        """Выбирает первый вариант ответа (чтобы пройти дальше)."""
        opts = page.locator(".otp-item-view-question label.otp-input")
        if opts.count():
            OTPClient._click_robust(opts.first)
            return
        for sel in (".otp-item-view-question input[type=text]",
                    ".otp-item-view-question input[type=number]",
                    ".otp-item-view-question textarea"):
            el = page.locator(sel)
            if el.count():
                try:
                    el.first.fill("0")
                except Exception:
                    pass
                return

    _QUESTION_JS = """
        () => {
            const q = document.querySelector('.otp-item-view-question');
            if (!q) return { qtext: '' };
            const qt = q.querySelector('.qtext');
            const qtext = qt ? qt.innerText.trim() : '';
            const qid = (q.id || '').replace(/^dq_/, '');
            const options = [];
            q.querySelectorAll('label.otp-input').forEach(l => {
                const inp = l.querySelector('input');
                const span = l.querySelector('span');
                options.push({
                    type: inp ? inp.type : 'option',
                    text: (span ? span.innerText : l.innerText).trim()
                });
            });
            const extraInputs = [...q.querySelectorAll(
                'input[type=text], input[type=number], textarea, select'
            )].map(e => ({
                tag: e.tagName.toLowerCase(),
                type: e.type || '',
                id: e.id || '',
                cls: String(e.className || '')
            }));
            let qtype = 'other';
            if (q.querySelector('input[type=radio]')) qtype = 'single';
            else if (q.querySelector('input[type=checkbox]')) qtype = 'multiple';
            else if (q.querySelector('textarea')) qtype = 'text';
            else if (q.querySelector('select')) qtype = 'select';
            else if (q.querySelector('input[type=text], input[type=number]')) qtype = 'input';
            return { qid, qtext, qtype, options, extraInputs };
        }
    """

    # ---------------------------------------------------------------
    # Список тестов кабинета (для сопоставления по названию)
    # ---------------------------------------------------------------
    def fetch_account_tests(self):
        return self._run(self._impl_fetch_account_tests)

    def _impl_fetch_account_tests(self):
        """Возвращает список всех тестов кабинета: [{id, title}]."""
        with self._lock:
            self._start()
            if not self.connected:
                raise OTPError("Нет сессии в личном кабинете.")
            page = self._page
            page.goto(TESTS_URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(1500)
            tests = []
            seen = set()
            for _ in range(30):
                page.wait_for_timeout(700)
                data = page.evaluate(self._ACCT_TESTS_JS)
                added = 0
                for t in data.get("tests", []):
                    key = (t["id"], t["title"])
                    if key not in seen:
                        seen.add(key)
                        tests.append(t)
                        added += 1
                if not self._click_next_page(page):
                    break
            return tests

    @staticmethod
    def _click_next_page(page):
        """Кликает по следующей странице списка тестов. True — если перешли."""
        try:
            return page.evaluate("""() => {
                const items = [...document.querySelectorAll('.pagination a, .pagination span')];
                let cur = null;
                for (const el of items) {
                    const t = parseInt((el.innerText || '').trim(), 10);
                    if (t && el.closest('.active, li.active')) { cur = t; break; }
                }
                if (!cur) return false;
                for (const el of items) {
                    const t = parseInt((el.innerText || '').trim(), 10);
                    if (t === cur + 1) { el.click(); return true; }
                }
                return false;
            }""")
        except Exception:
            return False

    _ACCT_TESTS_JS = """
        () => {
            const out = { tests: [] };
            const seen = new Set();
            for (const a of document.querySelectorAll('a[href]')) {
                const h = a.getAttribute('href') || '';
                const m = h.match(/\\/tests\\/([a-z0-9]{6,})(?:\\?|$)/);
                if (!m) continue;
                const t = (a.innerText || a.getAttribute('title') || '').trim().replace(/\\s+/g, ' ');
                if (!t) continue;
                const k = m[1] + '|' + t;
                if (seen.has(k)) continue;
                seen.add(k);
                out.tests.push({ id: m[1], title: t });
            }
            return out;
        }
    """

    @staticmethod
    def _norm_name(s):
        s = (s or "").lower()
        s = re.sub(r"[^\w\s]", "", s, flags=re.UNICODE)
        return re.sub(r"\s+", " ", s).strip()

    def _resolve_account_test(self, url, name):
        """Находит id теста в кабинете по названию (публичная ссылка и id
        кабинета могут не совпадать). Возвращает id или исходный id из url."""
        m = re.search(r"onlinetestpad\.com/([A-Za-z0-9]+)", url)
        url_id = m.group(1) if m else None
        if not self._account_tests_cache:
            try:
                self._account_tests_cache = self.fetch_account_tests()
            except Exception:
                return url_id
        target = self._norm_name(name or "")
        if not target:
            return url_id
        best = None
        best_score = -1
        for t in self._account_tests_cache:
            tn = self._norm_name(t["title"])
            if not tn:
                continue
            if tn == target:
                return t["id"]
            # частичное совпадение: одно название содержит другое
            if target in tn or tn in target:
                score = min(len(target), len(tn)) / max(len(target), len(tn), 1)
                if score > best_score:
                    best_score = score
                    best = t["id"]
        return best or url_id

    # ---------------------------------------------------------------
    # Статистика ответов по тесту
    # ---------------------------------------------------------------
    def fetch_test_statistics(self, url, sub="answers", name=None):
        return self._run(self._impl_fetch_test_statistics, url, sub, name)

    def _impl_fetch_test_statistics(self, url, sub="answers", name=None):
        """Скачивает таблицу ответов студентов по тесту.

        Для этого нужен вход в личный кабинет: страница статистики доступна
        только авторизованному владельцу теста. При sub="summary" дополнительно
        собирает ключ правильных ответов из редактора вопросов и сопоставляет
        с ответами студентов — возвращает готовую структуру для визуализации.
        """
        with self._lock:
            self._start()
            if not self.connected:
                raise OTPError("Нет сессии в личном кабинете. Сначала войдите.")
            test_id = self._resolve_account_test(url, name)
            if not test_id:
                raise OTPError("Не удалось определить id теста из ссылки.")
            page = self._page

            if sub == "summary":
                return self._load_summary(page, test_id)

            page.goto(f"{BASE}/tests/{test_id}/statistics/{sub}",
                      wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2500)  # ждём ajax-загрузку таблицы
            if "account/login" in page.url or page.locator("#txtEmail").count():
                # сессия истекла — сбрасываем сохранённое состояние
                self._clear_state()
                raise OTPError("Сессия в личном кабинете истекла. Войдите заново.")
            data = page.evaluate(self._STATS_JS)
            data["test_id"] = test_id
            data["page_title"] = page.title()
            data["final_url"] = page.url
            return data

    def _load_summary(self, page, test_id):
        """Собирает реальные результаты: ключ ответов из редактора вопросов
        и матрицу ответов студентов со страницы /statistics/summary."""
        # 1) ключ правильных ответов из редактора вопросов
        page.goto(f"{BASE}/tests/{test_id}/questions",
                  wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        key = page.evaluate(self._ANSWER_KEY_JS)

        # 2) таблица ответов студентов (ждём появления с опросом)
        page.goto(f"{BASE}/tests/{test_id}/statistics/summary",
                  wait_until="domcontentloaded", timeout=30000)
        data = None
        for _ in range(20):  # до 10 секунд
            page.wait_for_timeout(500)
            try:
                data = page.evaluate(self._SUMMARY_JS)
                if data.get("found"):
                    break
            except Exception:
                data = None
        if "account/login" in page.url or page.locator("#txtEmail").count():
            self._clear_state()
            raise OTPError("Сессия в личном кабинете истекла. Войдите заново.")
        if not data or not data.get("found"):
            # пробуем ещё раз с перезагрузкой
            page.goto(f"{BASE}/tests/{test_id}/statistics/summary",
                      wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
            try:
                data = page.evaluate(self._SUMMARY_JS)
            except Exception:
                data = None
        if not data or not data.get("found"):
            return {
                "test_id": test_id,
                "final_url": page.url,
                "page_title": page.title(),
                "questions": key.get("questions", []),
                "students": [],
                "summary": {"completed": 0, "total": 0, "avg_percent": 0, "avg_score": 0, "max_score": len(key.get("questions", [])) or 1},
                "mode": "summary",
                "notice": "Таблица ответов студентов не найдена на странице статистики.",
            }

        questions = key.get("questions", [])
        students = []
        for s in data.get("students", []):
            answers = []
            for i, a in enumerate(s.get("answers", [])):
                q = questions[i] if i < len(questions) else None
                correct = False
                if q:
                    opt = next((o for o in q.get("options", []) if o.get("idx") == a.get("num")), None)
                    correct = bool(opt and opt.get("correct"))
                answers.append({**a, "correct": correct})
            correct_count = sum(1 for a in answers if a.get("correct"))
            # процент считаем от известного числа вопросов
            percent = round(correct_count / len(questions) * 100) if questions else (s.get("percent") or 0)
            students.append({**s, "correct": correct_count, "percent": percent, "answers": answers})

        completed = [s for s in students if s.get("finished")]
        summary = {
            "completed": len(completed),
            "total": len(students),
            "avg_percent": round(sum(s["percent"] for s in completed) / len(completed)) if completed else 0,
            "avg_score": round(sum(s["correct"] for s in completed) / len(completed)) if completed else 0,
            "max_score": len(questions) or 1,
        }
        return {
            "test_id": test_id,
            "final_url": page.url,
            "page_title": page.title(),
            "questions": questions,
            "students": students,
            "summary": summary,
            "mode": "summary",
        }

    _ANSWER_KEY_JS = """
        () => {
            const out = { questions: [] };
            for (const q of document.querySelectorAll('[id^=qid_]')) {
                const qtext = (q.querySelector('.qtext') || {});
                const text = (qtext.innerText || '').trim().replace(/\\s+/g, ' ');
                if (!text) continue;
                const options = [...q.querySelectorAll('label.otp-input')].map((l, i) => ({
                    idx: i + 1,
                    text: (l.innerText || '').trim().replace(/\\s+/g, ' '),
                    correct: !!l.querySelector('.icon-rb-checked, .icon-cb-checked')
                }));
                out.questions.push({ text, options });
            }
            return out;
        }
    """

    _SUMMARY_JS = """
        () => {
            const tables = [...document.querySelectorAll('table')];
            const t = tables.find(t => /table-hover/.test(t.className || ''));
            if (!t) return { found: false, students: [], qHeaders: [] };
            const theadRows = [...t.querySelectorAll('thead tr')];
            let qCount = 0;
            let qHeaders = [];
            if (theadRows.length > 1) {
                const items = theadRows[1].querySelectorAll('th.item');
                qCount = items.length;
                qHeaders = [...items].map(th => (th.innerText || '').trim().replace(/\\s+/g, ' '));
            }
            const rows = [...t.querySelectorAll('tbody tr')];
            if (!rows.length) return { found: false, students: [], qHeaders };
            if (!qCount) {
                const first = [...rows[0].querySelectorAll('td')];
                qCount = Math.max(0, first.length - 10);
            }
            const students = [];
            for (const tr of rows) {
                const tds = [...tr.querySelectorAll('td')];
                if (tds.length < 10) continue;
                const get = i => tds[i] ? (tds[i].innerText || '').trim().replace(/\\s+/g, ' ') : '';
                const answers = tds.slice(tds.length - qCount).map(c => {
                    const numEl = c.querySelector('.fs-12');
                    const txtEl = c.querySelector('.ans-text-value');
                    return {
                        num: numEl ? parseInt(numEl.innerText, 10) : null,
                        text: (txtEl ? txtEl.innerText : c.innerText).trim().replace(/\\s+/g, ' ')
                    };
                });
                students.push({
                    attempt: get(1), user: get(3), ip: get(4), date: get(5), time: get(6),
                    finished: get(7).trim() === 'К', correct: parseInt(get(8), 10) || 0,
                    percent: parseFloat(get(9)) || 0, answers
                });
            }
            return { found: students.length > 0, qHeaders, students };
        }
    """

    _STATS_JS = """
        () => {
            const out = { tables: [], buttons: [], links: [] };
            document.querySelectorAll('table').forEach((t, ti) => {
                const rows = [...t.querySelectorAll('tr')].map(tr =>
                    [...tr.querySelectorAll('th,td')].map(c =>
                        (c.innerText || '').trim().replace(/\\s+/g, ' ')));
                out.tables.push({ index: ti, cls: String(t.className || ''), rows });
            });
            for (const b of document.querySelectorAll('a,button')) {
                const txt = (b.innerText || b.getAttribute('title') || '').trim().replace(/\\s+/g, ' ').slice(0, 60);
                if (txt) out.buttons.push({ text: txt, href: b.getAttribute('href') || '' });
                if (out.buttons.length > 60) break;
            }
            return out;
        }
    """

    # ---------------------------------------------------------------
    # Диагностика
    # ---------------------------------------------------------------
    def diagnostics(self):
        return self._run(self._impl_diagnostics)

    def _impl_diagnostics(self):
        """Возвращает текущую страницу и образцы ссылок — для отладки парсера."""
        with self._lock:
            if not self._page:
                return {"connected": False}
            page = self._page
            return {
                "connected": self.connected,
                "login_url": LOGIN_URL,
                "url": page.url,
                "title": page.title(),
                "last_dump": getattr(self, "_last_dump", None),
                "sample": page.evaluate(self._EXTRACT_JS),
            }