"use strict";

/* ============================================================
   ДЕМО-ДАННЫЕ (для раздела «Анализ результатов»)
   Ответы: 1 = верно, 0 = ошибка
   ============================================================ */
const DEMO_DATA = {
  disciplines: [
    {
      name: "Информатика",
      tests: [
        {
          id: 101,
          name: "Вводное тестирование по информатике",
          questions: [
            { topic: "Аппаратное обеспечение", text: "Что такое процессор?" },
            { topic: "Информация", text: "Сколько бит в одном байте?" },
            { topic: "Аппаратное обеспечение", text: "Что означает аббревиатура ОЗУ?" },
            { topic: "Аппаратное обеспечение", text: "Какое устройство является устройством ввода?" },
            { topic: "Алгоритмы", text: "Что такое алгоритм?" },
            { topic: "Программирование", text: "Какой язык программирования является низкоуровневым?" },
            { topic: "Файловая система", text: "Что такое файл?" },
            { topic: "Веб", text: "Что означает аббревиатура HTML?" },
            { topic: "Программное обеспечение", text: "Что такое операционная система?" },
            { topic: "Медиа", text: "Какой из форматов является графическим?" }
          ],
          students: [
            { name: "Иванова А.", answers: [1,1,1,1,1,0,1,1,1,1] },
            { name: "Петров С.", answers: [1,1,0,1,1,0,1,0,1,0] },
            { name: "Сидоров М.", answers: [1,1,1,1,1,1,1,1,1,1] },
            { name: "Козлов Д.", answers: [0,1,1,0,1,0,0,0,0,0] },
            { name: "Смирнова Е.", answers: [1,1,1,1,0,0,1,1,1,1] },
            { name: "Волков А.", answers: [1,0,0,1,1,0,1,0,1,1] },
            { name: "Морозова К.", answers: [1,1,0,1,1,1,1,0,1,0] },
            { name: "Новиков И.", answers: [0,1,0,0,0,0,1,0,0,0] }
          ]
        },
        {
          id: 102,
          name: "Алгоритмы и программирование",
          questions: [
            { topic: "Алгоритмы", text: "Что такое алгоритм?" },
            { topic: "Программирование", text: "Какой оператор используется для вывода данных?" },
            { topic: "Программирование", text: "Что такое переменная?" },
            { topic: "Алгоритмы", text: "Что такое цикл?" },
            { topic: "Программирование", text: "Какой оператор используется для ветвления?" },
            { topic: "Структуры данных", text: "Что такое массив?" },
            { topic: "Программирование", text: "Какой язык программирования интерпретируемый?" },
            { topic: "Программирование", text: "Что такое функция?" }
          ],
          students: [
            { name: "Соколов А.", answers: [1,1,1,1,1,1,1,1] },
            { name: "Богданова О.", answers: [1,1,0,1,1,1,1,1] },
            { name: "Романов П.", answers: [1,0,1,1,0,1,0,1] },
            { name: "Лебедев К.", answers: [1,0,0,0,1,1,0,0] },
            { name: "Фёдорова М.", answers: [1,1,1,1,1,1,1,1] },
            { name: "Орлов Д.", answers: [1,1,0,1,0,0,1,1] }
          ]
        },
        {
          id: 103,
          name: "Компьютерные сети и веб",
          questions: [
            { topic: "Сети", text: "Что такое IP-адрес?" },
            { topic: "Веб", text: "Что такое протокол HTTP?" },
            { topic: "Веб", text: "Что такое домен?" },
            { topic: "Безопасность", text: "Что такое файрвол?" },
            { topic: "Веб", text: "Что такое cookie?" },
            { topic: "Сети", text: "Что такое DNS?" },
            { topic: "Безопасность", text: "Что такое шифрование?" }
          ],
          students: [
            { name: "Громов И.", answers: [1,1,1,1,1,1,1] },
            { name: "Кузнецова П.", answers: [1,0,1,1,0,1,1] },
            { name: "Ефимов Т.", answers: [1,1,0,0,1,1,0] },
            { name: "Абрамова В.", answers: [0,0,1,1,1,0,0] },
            { name: "Тихонов С.", answers: [1,0,1,0,1,1,1] }
          ]
        }
      ]
    },
    {
      name: "Математика",
      tests: [
        {
          id: 201,
          name: "Математика. Входной контроль",
          questions: [
            { topic: "Алгебра", text: "Решите уравнение: 2x + 5 = 15." },
            { topic: "Геометрия", text: "Чему равна площадь прямоугольника со сторонами 4 и 7?" },
            { topic: "Алгебра", text: "Вычислите: 3² + 4²." },
            { topic: "Тригонометрия", text: "Чему равен sin(90°)?" },
            { topic: "Математический анализ", text: "Что такое производная функции?" },
            { topic: "Алгебра", text: "Решите неравенство: x − 3 > 7." },
            { topic: "Геометрия", text: "Чему равна сумма углов треугольника?" },
            { topic: "Проценты", text: "Вычислите: 25% от 200." },
            { topic: "Алгебра", text: "Что такое логарифм?" },
            { topic: "Математический анализ", text: "Чему равен интеграл от x?" }
          ],
          students: [
            { name: "Михайлов Е.", answers: [1,1,1,0,1,1,1,1,1,1] },
            { name: "Андреева Л.", answers: [1,1,1,1,0,1,1,1,1,0] },
            { name: "Захаров Н.", answers: [1,0,1,0,0,1,0,1,0,0] },
            { name: "Павлова Д.", answers: [1,1,1,1,1,1,1,1,1,1] },
            { name: "Семёнов О.", answers: [1,1,0,0,1,0,1,1,0,0] },
            { name: "Григорьев Т.", answers: [1,1,1,1,0,1,0,1,0,1] },
            { name: "Володина М.", answers: [0,0,1,0,0,0,1,1,0,0] }
          ]
        }
      ]
    }
  ]
};

/* ============================================================
   УТИЛИТЫ
   ============================================================ */
const $ = (sel) => document.querySelector(sel);
const esc = (s) => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const pct = (x) => Math.round(x * 100);
function normUrl(s) {
  const m = String(s || "").match(/onlinetestpad\.com[^\s"'<>]*/);
  return m ? "https://" + m[0].replace(/^https?:\/\//, "") : String(s || "").trim();
}
function colorFor(rate) {
  if (rate >= 0.8) return "var(--green)";
  if (rate >= 0.6) return "var(--amber)";
  return "var(--red)";
}

/* ============================================================
   МОДЕЛЬ (демо): анализ ответов студентов
   ============================================================ */
function analyzeTest(test) {
  const qs = test.questions;
  const sts = test.students;
  const qCount = qs.length, n = sts.length;

  const perQuestion = qs.map((q, qi) => {
    let correct = 0; const wrong = [];
    sts.forEach(s => { if (s.answers[qi]) correct++; else wrong.push(s.name); });
    return { idx: qi, text: q.text, topic: q.topic, correct, wrong, rate: correct / n };
  });

  const perStudent = sts.map(s => {
    const correct = s.answers.reduce((a, b) => a + b, 0);
    return { name: s.name, answers: s.answers, correct, rate: correct / qCount, wrongCount: qCount - correct };
  }).sort((a, b) => b.correct - a.correct);

  const topicMap = {};
  perQuestion.forEach(q => {
    const t = (topicMap[q.topic] ||= { name: q.topic, correct: 0, total: 0, qs: 0 });
    t.correct += q.correct; t.total += n; t.qs += 1;
  });
  const topics = Object.values(topicMap).map(t => ({ ...t, rate: t.total ? t.correct / t.total : 0 }))
    .sort((a, b) => a.rate - b.rate);
  const weakTopics = topics.filter(t => t.rate < 0.7);

  const repeats = [];
  weakTopics.forEach(t => {
    const qIdx = perQuestion.filter(q => q.topic === t.name).map(q => q.idx);
    const hits = sts.map(s => ({ name: s.name, missed: qIdx.filter(i => !s.answers[i]).length }))
      .filter(h => h.missed > 0 && h.missed >= Math.ceil(qIdx.length / 2))
      .sort((a, b) => b.missed - a.missed);
    if (hits.length) repeats.push({ topic: t.name, students: hits, questions: qIdx });
  });

  const failCount = {};
  repeats.forEach(r => r.students.forEach(h => failCount[h.name] = (failCount[h.name] || 0) + 1));
  const riskGroup = Object.entries(failCount).filter(([, c]) => c >= 2).map(([name]) => name).sort();

  const buckets = [
    { label: "0–20", min: 0, max: 20, count: 0 },
    { label: "21–40", min: 21, max: 40, count: 0 },
    { label: "41–60", min: 41, max: 60, count: 0 },
    { label: "61–80", min: 61, max: 80, count: 0 },
    { label: "81–100", min: 81, max: 100, count: 0 }
  ];
  perStudent.forEach(s => {
    const p = Math.round(s.rate * 100);
    buckets.forEach(b => { if (p >= b.min && p <= b.max) b.count++; });
  });

  return {
    test, perQuestion, perStudent, topics, weakTopics, repeats, riskGroup,
    buckets,
    avg: Math.round(perStudent.reduce((a, s) => a + s.rate, 0) / n * 100),
    median: (() => { const p = perStudent.map(s => s.rate * 100).sort((a, b) => a - b); const m = Math.floor(n / 2); return n % 2 ? p[m] : Math.round((p[m - 1] + p[m]) / 2); })(),
    passed: perStudent.filter(s => s.rate >= 0.6).length,
    failed: perStudent.filter(s => s.rate < 0.6).length
  };
}

/* ============================================================
   РЕНДЕРИНГ
   ============================================================ */

let fileData = null;        // data/tests.json / Excel
let fileState = { discipline: null, test: null };
let quality = null;         // последний результат анализа качества
let qaFilter = "all";
let demoTest = DEMO_DATA.disciplines[0].tests[0];
let realResults = null;     // реальная статистика по выбранному тесту
let analyzing = false;      // идёт ли обход/анализ теста

/* --- файл ссылок (дисциплины и тесты) --- */

async function loadTestsFile() {
  let j;
  try {
    const r = await fetch("/api/tests-file");
    j = await r.json();
  } catch (e) {
    $("#disciplineList").innerHTML = `<li class="empty">Сервер не отвечает. Запустите server.py</li>`;
    return;
  }
  if (!j.ok) {
    $("#disciplineList").innerHTML = `<li class="empty">Ошибка загрузки: ${esc(j.error || r.status)}</li>`;
    return;
  }
  fileData = j;
  if (j.disciplines && j.disciplines.length) {
    fileState.discipline = j.disciplines[0];
    fileState.test = null;
  }
  renderFileDisciplines();
  renderFileTests();
}

function renderFileDisciplines() {
  const ul = $("#disciplineList");
  ul.innerHTML = (fileData && fileData.disciplines || []).map(d =>
    `<li class="${d.name === fileState.discipline?.name ? "selected" : ""}" data-name="${esc(d.name)}">
       <div class="title">${esc(d.name)}</div>
       <div class="sub">${d.tests.length} тестов</div>
     </li>`).join("") || '<li class="empty">В файле data/tests.json нет дисциплин</li>';
}

function renderFileTests() {
  const ul = $("#testList");
  ul.innerHTML = (fileState.discipline?.tests || []).map(t => {
    const sel = t.url === fileState.test?.url ? "selected" : "";
    const running = analyzing && sel ? " running" : "";
    return `<li class="${sel}${running}" data-url="${esc(t.url)}">
       <div class="title">${esc(t.name)}${running ? '<span class="run-badge">анализируется…</span>' : ""}</div>
       <div class="sub">${t.url.replace(/^https?:\/\//, "").slice(0, 45)}…</div>
     </li>`;
  }).join("") || '<li class="empty">В папке нет тестов</li>';
}

/* --- анализ качества теста --- */

async function analyzeQuality(test) {
  if (analyzing) {
    showQaError("Уже выполняется анализ другого теста. Дождитесь завершения.");
    return;
  }
  analyzing = true;
  $("#qaError").hidden = true;
  $("#qaResult").hidden = true;
  fileState.test = test;         // запоминаем анализируемый тест (для результатов)
  renderFileTests();             // подсветить выбранный/анализируемый тест
  const btn = $("#btnQaRun");
  const oldText = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Анализ…";
  const st = $("#qaStatus");
  st.hidden = false;
  $("#qaStatusText").textContent = (test.name || test.url || "Тест");
  $("#qaStatusSub").textContent = test.url + " · обход до минуты";
  try {
    const r = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: test.url })
    });
    const j = await r.json();
    if (!j.ok) { showQaError(j.error || "Ошибка анализа"); return; }
    quality = j;
    renderQuality(j);
    switchTo("quality");
  } catch (e) {
    showQaError("Сервер не отвечает: " + e.message);
  } finally {
    analyzing = false;
    renderFileTests();
    btn.disabled = false;
    btn.textContent = oldText;
    st.hidden = true;
  }
}

function showQaError(msg) {
  const el = $("#qaError");
  el.textContent = msg;
  el.hidden = false;
}

function renderQuality(j) {
  $("#qaResult").hidden = false;
  $("#testTitle").textContent = j.title || "Анализ теста";
  $("#testMeta").textContent = `${j.count} вопросов · оценка качества ${j.score}/100 · средняя сложность ${j.avg_difficulty}/5`;

  // сводные карточки
  const levelTxt = j.score >= 80 ? "хороший" : j.score >= 60 ? "средний" : "низкий";
  $("#qaCards").innerHTML = `
    <div class="card ${j.score >= 60 ? "green" : "red"}"><div class="k">Оценка качества</div><div class="v">${j.score}/100</div><div class="d">${levelTxt} уровень</div></div>
    <div class="card"><div class="k">Вопросов</div><div class="v">${j.count}</div><div class="d">${j.count ? "по ссылке" : ""}</div></div>
    <div class="card amber"><div class="k">Средняя сложность</div><div class="v">${j.avg_difficulty}/5</div></div>
    <div class="card ${j.issues_total.alert ? "red" : "green"}"><div class="k">Требуют правки</div><div class="v">${j.issues_total.alert}</div><div class="d">замечаний: ${j.issues_total.warn}</div></div>`;

  // типы вопросов
  const typeRows = Object.entries(j.type_counts || {}).sort((a, b) => b[1] - a[1]);
  const maxT = Math.max(1, ...typeRows.map(([, v]) => v));
  $("#qaTypes").innerHTML = typeRows.map(([k, v]) => `
    <div class="type-row">
      <span class="t-name">${esc(k)}</span>
      <span class="t-val">${v}</span>
      <div class="t-track"><div class="t-fill" style="width:${v / maxT * 100}%;background:var(--accent)"></div></div>
    </div>`).join("") || '<div class="empty-note">Нет данных</div>';

  // распределение сложности
  const diff = j.difficulty_dist || {};
  const maxD = Math.max(1, ...Object.values(diff));
  $("#qaDifficulty").innerHTML = [1, 2, 3, 4, 5].map(l => {
    const v = diff[l] || 0;
    return `
    <div class="type-row">
      <span class="t-name">Уровень ${l}</span>
      <span class="t-val">${v}</span>
      <div class="t-track"><div class="t-fill" style="width:${v / maxD * 100}%;background:${l >= 4 ? "var(--red)" : l >= 3 ? "var(--amber)" : "var(--green)"}"></div></div>
    </div>`;
  }).join("");

  // ключевые понятия
  const chips = [...(j.keywords || []), ...(j.dominant_words || [])]
    .filter((v, i, a) => a.indexOf(v) === i).slice(0, 20);
  $("#qaKeywords").innerHTML = (j.themes && j.themes.length
    ? `<span class="kw-chip kw-theme">тема: ${j.themes.map(esc).join(", ")}</span>` : "")
    + chips.map(k => `<span class="kw-chip">${esc(k)}</span>`).join("")
    || '<div class="empty-note">Не удалось выделить понятия</div>';

  // рекомендации
  const kindLabels = {
    simplify: "Упростить", complicate: "Усложнить", add: "Добавить",
    topic: "Тема", professional: "Стиль", general: "Итог"
  };
  $("#qaRecommendations").innerHTML = (j.recommendations || []).map((r, i) => `
    <div class="rec">
      <div class="rec-num">${i + 1}</div>
      <div class="rec-body"><span class="rec-kind k-${r.kind}">${kindLabels[r.kind] || r.kind}</span> ${esc(r.text)}</div>
    </div>`).join("") || '<div class="empty-note">Замечаний нет</div>';

  // вопросы
  renderQaQuestions();
}

const VERDICT_LABEL = { ok: "Норма", warn: "Замечания", alert: "Правка" };

function renderQaQuestions() {
  const list = (quality?.questions || []).filter(q =>
    qaFilter === "all" ? true : q.verdict === qaFilter);
  $("#qaQuestions").innerHTML = list.map(q => `
    <details class="q-card v-${q.verdict}" data-verdict="${q.verdict}">
      <summary>
        <span class="q-num">В${q.idx + 1}</span>
        <span class="badge t-${q.qtype}">${esc(q.qtype_label)}</span>
        <span class="q-text">${esc(q.text)}</span>
        <span class="diff">сл. ${q.difficulty}/5</span>
        <span class="verdict v-${q.verdict}">${VERDICT_LABEL[q.verdict]}</span>
      </summary>
      <div class="q-body">
        ${q.options && q.options.length ? `<div class="q-opts">${q.options.map((o, i) =>
          `<div class="opt"><span class="opt-mark">${o.type === "checkbox" ? "☐" : "◉"}</span>${esc(o.text)}</div>`).join("")}</div>` : ""}
        <div class="q-issues">
          ${q.issues && q.issues.length ? q.issues.map(i =>
            `<div class="issue i-${i.level}">${i.level === "alert" ? "⚠" : "·"} ${esc(i.text)}</div>`).join("")
            : '<div class="issue i-ok">Замечаний нет</div>'}
        </div>
      </div>
    </details>`).join("") || '<div class="empty-note">Нет вопросов с таким вердиктом</div>';
}

/* --- демо: анализ результатов группы --- */

function renderDemoSelect() {
  const sel = $("#demoTestSelect");
  let html = `<option value="file">Тест из п.1 (последний анализ)</option>`;
  html += DEMO_DATA.disciplines.map(d =>
    `<optgroup label="${esc(d.name)}">` + d.tests.map(t =>
      `<option value="${t.id}">${esc(t.name)}</option>`).join("") + `</optgroup>`).join("");
  sel.innerHTML = html;
  sel.value = "file";
}

function topicFor(q) {
  const low = (q.text || "").toLowerCase();
  const terms = (quality && quality.topic_terms) || [];
  const hit = terms.find(t => low.includes(t));
  return hit || "Общие понятия";
}

function syntheticStudents(questions, n) {
  const names = ["Иванова А.", "Петров С.", "Сидоров М.", "Козлов Д.", "Смирнова Е.",
    "Волков А.", "Морозова К.", "Новиков И.", "Лебедев К.", "Фёдорова М."];
  const students = [];
  for (let i = 0; i < n; i++) {
    let s = 1000 + i * 131;
    const rnd = () => (s = (s * 9301 + 49297) % 233280) / 233280;
    const ability = 0.45 + (i % 5) * 0.09 + rnd() * 0.1;
    const answers = questions.map((q, j) => {
      const diff = (quality && quality.questions && quality.questions[j]) ? quality.questions[j].difficulty : 2;
      const p = Math.max(0.05, Math.min(0.98, ability - (diff - 1) * 0.12 - rnd() * 0.15));
      return rnd() < p ? 1 : 0;
    });
    students.push({ name: names[i % names.length], answers });
  }
  return students;
}

function currentResultsTest() {
  if (realResults) return realResults;
  const sel = $("#demoTestSelect").value;
  if (sel === "file") {
    if (fileState.test && quality && quality.questions && quality.questions.length) {
      const qs = quality.questions.map(q => ({ text: q.text, topic: topicFor(q) }));
      return { name: fileState.test.name, questions: qs, students: syntheticStudents(qs, 8) };
    }
    return null;
  }
  return DEMO_DATA.disciplines.flatMap(d => d.tests).find(t => String(t.id) === sel) || demoTest;
}

/* --- реальная статистика из кабинета --- */

function guessCorrect(cell) {
  const s = String(cell || "").trim();
  if (!s) return 0;
  if (/^(✓|✔|да|yes|1|верно|правильно)$/i.test(s)) return 1;
  if (/^(✗|✘|×|нет|no|0|неверно)$/i.test(s)) return 0;
  return 1;
}

function parseStats(j, quality) {
  const tables = (j.tables || []).filter(t => t.rows && t.rows.length > 1);
  if (!tables.length) return null;
  tables.sort((a, b) =>
    (b.rows[0] || []).length - (a.rows[0] || []).length || b.rows.length - a.rows.length);
  const rows = tables[0].rows;
  const header = rows[0];
  const ncols = header.length;
  // последние столбцы с «%» / «Оценка» / «Время» — не вопросы
  let qCount = 0;
  const qCols = [];
  for (let c = 1; c < ncols; c++) {
    const h = String(header[c] || "").toLowerCase();
    if (/^(%|оценк|балл|результат|время|вопрос|правильн)/.test(h) && qCols.length) break;
    if (qCols.length && !/^[0-9]+$/.test(h) && !/^в\d+$/i.test(h) && !/^q\d+$/i.test(h)) break;
    qCols.push(c);
  }
  const nq = qCols.length;
  if (!nq) return null;

  const students = [];
  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (!r || !r.length) continue;
    const name = (r[0] || "").trim();
    if (!name || /^(итог|средн|средний|всего|номер)/i.test(name)) continue;
    const answers = qCols.map(c => guessCorrect(r[c] || ""));
    students.push({ name, answers });
  }
  if (!students.length) return null;

  const qtexts = (quality && quality.questions) || [];
  const questions = qCols.map((c, i) => ({
    text: (qtexts[i] && qtexts[i].text) ? qtexts[i].text : (header[c] || "Вопрос " + (i + 1)),
    topic: qtexts[i] ? topicFor(qtexts[i]) : "—"
  }));
  const name = (fileState.test && fileState.test.name) || "Тест";
  return { name, questions, students };
}

function showDemoNotice(msg) {
  const notice = $("#demoNotice");
  notice.hidden = false;
  notice.textContent = msg;
}

async function loadRealStats() {
  const test = fileState.test;
  if (!test) { showDemoNotice("Сначала выберите тест в разделе «Дисциплины и тесты»."); return; }
  const btn = $("#btnLoadStats");
  const btnDemo = $("#btnLoadDemo");
  const old = btn.textContent;
  btn.disabled = true;
  btnDemo.disabled = true;
  btn.textContent = "Загрузка статистики…";
  const st = $("#statsStatus");
  st.hidden = false;
  $("#statsStatusText").textContent = "Загружаем статистику…";
  $("#statsStatusSub").textContent = (test.name || test.url || "Тест") + " · ключ ответов + таблица студентов";
  try {
    const r = await fetch("/api/statistics", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: test.url, name: test.name, sub: "summary" })
    });
    const j = await r.json();
    if (!j.ok) {
      if (/сесси/i.test(j.error || "")) {
        await refreshStatus();   // синхронизировать индикатор кабинета
        showDemoNotice("Кабинет не подключён. Нажмите «Подключить кабинет» и войдите в onlinetestpad.");
      } else {
        showDemoNotice(j.error || "Ошибка загрузки статистики");
      }
      return;
    }
    if (j.mode === "summary" && j.students && j.students.length) {
      realResults = j;
      $("#demoTestSelect").value = "file";
      renderRealResults(j);
      showDemoNotice(`Загружены реальные результаты: ${j.summary.completed} завершённых попыток, ${j.summary.total} всего, средний балл ${j.summary.avg_percent}%.`);
    } else {
      showDemoNotice("Не удалось разобрать таблицу статистики. Возможно, по тесту ещё нет завершённых прохождений.");
    }
  } catch (err) {
    showDemoNotice("Сервер не отвечает: " + err.message);
  } finally {
    btn.disabled = false;
    btnDemo.disabled = false;
    btn.textContent = old;
    st.hidden = true;
  }
}

function renderRealResults(j) {
  const questions = j.questions || [];
  const students = j.students || [];
  const sum = j.summary || {};

  $("#testTitle").textContent = (j.page_title || "Анализ результатов").replace(/\s*-\s*Online Test Pad$/, "") + " — реальные результаты";
  const disc = fileState.discipline ? fileState.discipline.name : "";
  $("#testMeta").textContent = `${disc} · ${sum.completed} завершённых из ${sum.total} попыток · ${questions.length} вопросов`;

  // сводные карточки
  const avgScore = sum.avg_score || 0;
  const maxScore = sum.max_score || questions.length || 1;
  $("#summaryCards").innerHTML = `
    <div class="card"><div class="k">Завершённых попыток</div><div class="v">${sum.completed}</div><div class="d">всего попыток: ${sum.total}</div></div>
    <div class="card"><div class="k">Средний балл</div><div class="v">${avgScore}/${maxScore}</div><div class="d">средний %: ${sum.avg_percent}%</div></div>
    <div class="card green"><div class="k">Сдали (≥60%)</div><div class="v">${students.filter(s => s.percent >= 60).length}</div><div class="d">не сдали: ${students.filter(s => s.percent < 60).length}</div></div>
    <div class="card ${sum.avg_percent < 60 ? "red" : "green"}"><div class="k">Средний результат</div><div class="v">${sum.avg_percent}%</div></div>
    <div class="card amber"><div class="k">Сложные вопросы</div><div class="v">${questions.filter((q, qi) => { const c = students.filter(s => s.answers[qi] && s.answers[qi].correct).length; return c / students.length < 0.6; }).length}</div><div class="d">верных &lt; 60%</div></div>`;

  // распределение результатов
  const buckets = [
    { label: "0–20", min: 0, max: 20, count: 0 },
    { label: "21–40", min: 21, max: 40, count: 0 },
    { label: "41–60", min: 41, max: 60, count: 0 },
    { label: "61–80", min: 61, max: 80, count: 0 },
    { label: "81–100", min: 81, max: 100, count: 0 }
  ];
  students.forEach(s => { const p = Math.round(s.percent); buckets.forEach(b => { if (p >= b.min && p <= b.max) b.count++; }); });
  const maxC = Math.max(1, ...buckets.map(b => b.count));
  $("#scoreChart").innerHTML = buckets.map(b => `
    <div class="col">
      <div class="lbl">${b.count}</div>
      <div class="bar ${b.max <= 40 ? "bad" : b.max <= 60 ? "warn" : ""}" style="height:${Math.max(6, b.count / maxC * 100)}%"></div>
      <div class="lbl">${b.label}</div>
    </div>`).join("");

  // проблемные вопросы по реальным данным
  const perQuestion = questions.map((q, qi) => {
    const correct = students.filter(s => s.answers[qi] && s.answers[qi].correct).length;
    return { idx: qi, text: q.text, correct, rate: students.length ? correct / students.length : 0 };
  });
  const sortedQ = [...perQuestion].sort((x, y) => x.rate - y.rate);
  $("#problemQuestions").innerHTML = sortedQ.map(q => {
    const color = colorFor(q.rate);
    const correctOpts = (questions[q.idx]?.options || []).filter(o => o.correct).map(o => o.text).join(", ") || "—";
    return `
    <div class="pq">
      <div class="pq-top">
        <span class="pq-q"><span class="qnum">В${q.idx + 1}</span>${esc(q.text)}</span>
        <span class="pq-rate" style="color:${color}">${pct(q.rate)}%</span>
      </div>
      <div class="pq-track"><div class="pq-fill" style="width:${pct(q.rate)}%;background:${color}"></div></div>
      <div class="pq-wrong">Верный ответ: ${esc(correctOpts)}</div>
    </div>`;
  }).join("");

  // матрица студент × вопрос
  const finished = students.filter(s => s.finished);
  const shown = finished.length ? finished : students;
  let table = `<table class="matrix">
    <thead><tr>
      <th>Студент</th>
      ${perQuestion.map((q, i) => `<th class="qhead ${q.rate < 0.6 ? "bad-q" : ""}" title="В${i + 1}. ${esc(q.text)}">В${i + 1}</th>`).join("")}
      <th>Верно</th><th>%</th>
    </tr></thead><tbody>`;
  shown.forEach(s => {
    const cls = s.percent < 60 ? " class=\"low\"" : "";
    table += `<tr${cls}>
      <td class="stu-name" title="${esc(s.attempt || s.user || s.ip)}">${esc(s.user || "Студент " + s.attempt)}</td>
      ${s.answers.map((a, i) => {
        const q = questions[i] || {};
        const opt = (q.options || []).find(o => o.idx === a.num) || {};
        const title = `${a.text || "нет ответа"} · верный: ${(q.options || []).filter(o => o.correct).map(o => o.text).join(", ") || "—"}`;
        const answered = a.num != null || (a.text && a.text.trim());
        return `<td class="${a.correct ? "ok" : answered ? "bad" : "none"}" title="${esc(title)}">${answered ? esc(a.text || a.num) : "—"}</td>`;
      }).join("")}
      <td class="score-cell">${s.correct}/${questions.length}</td>
      <td class="score-cell">${s.percent}%</td>
    </tr>`;
  });
  table += "</tbody></table>";
  $("#matrixTable").innerHTML = table;

  // темы: берём из анализа качества (topicFor), если есть
  const topicNames = (quality && quality.questions || []).map(q => topicFor(q));
  const topics = perQuestion.map((q, i) => ({ name: topicNames[i] || "Общие понятия", rate: q.rate }));
  const tmap = {};
  topics.forEach(t => { const x = tmap[t.name] ||= { name: t.name, c: 0, n: 0 }; x.c += t.rate; x.n++; });
  const topicBars = Object.values(tmap).map(t => ({ name: t.name, rate: t.c / t.n })).sort((a, b) => a.rate - b.rate);
  $("#topicsPanel").innerHTML = topicBars.map(t => {
    const color = colorFor(t.rate);
    return `
    <div class="topic">
      <span class="t-name">${esc(t.name)}</span>
      <span class="t-rate" style="color:${color}">${pct(t.rate)}%</span>
      <div class="t-track"><div class="t-fill" style="width:${pct(t.rate)}%;background:${color}"></div></div>
    </div>`;
  }).join("") || '<div class="empty-note">Нет данных</div>';

  // повторяющиеся ошибки по темам
  const repeats = topicBars.filter(t => t.rate < 0.7).map(t => {
    const qIdx = topics.map((x, i) => x.name === t.name ? i : -1).filter(i => i >= 0);
    const studentsMissed = shown.filter(s => qIdx.some(qi => s.answers[qi] && !s.answers[qi].correct));
    return { topic: t.name, questions: qIdx, students: studentsMissed };
  }).filter(r => r.students.length);
  $("#repeatsPanel").innerHTML = repeats.length ? repeats.map(r => {
    const qList = r.questions.map(i => `В${i + 1} — ${esc(questions[i]?.text || "")}`).join("<br>");
    const stuList = r.students.map(s => esc(s.user || s.attempt) + " (" + r.questions.filter(i => s.answers[i] && !s.answers[i].correct).length + " ошибок)").join("<br>");
    return `<div class="repeat">
      <div class="r-topic">Тема: ${esc(r.topic)}</div>
      <div class="r-q">${qList}</div>
      <div class="r-stu">${stuList}</div>
    </div>`;
  }).join("") : '<div class="empty-note">Повторяющихся ошибок по темам не выявлено</div>';

  // рекомендации
  const recs = [];
  const worst = perQuestion.filter(q => q.rate < 0.5).sort((a, b) => a.rate - b.rate);
  if (worst.length) recs.push(`<b>Самые проблемные вопросы:</b> ${worst.map(q => `В${q.idx + 1} «${esc(q.text)}» (${pct(q.rate)}% верных)`).join("; ")}. Разберите их на занятии, покажите верные ответы и попросите повторить тему.`);
  const weakTopics = topicBars.filter(t => t.rate < 0.6);
  if (weakTopics.length) recs.push(`<b>Слабые темы:</b> ${weakTopics.slice(0, 3).map(t => `«${esc(t.name)}» (${pct(t.rate)}%)`).join(", ")}. Повторите теорию и дайте тренировочные задания по этим темам.`);
  const lag = shown.filter(s => s.percent < 60).map(s => esc(s.user || "Студент " + s.attempt)).join(", ");
  if (lag) recs.push(`<b>Отстающие студенты:</b> ${lag}. Рекомендуется дополнительное задание или повторное прохождение после разбора ошибок.`);
  const best = [...shown].sort((a, b) => b.percent - a.percent)[0];
  if (best) recs.push(`<b>Лучший результат:</b> ${esc(best.user || "Студент " + best.attempt)} (${best.percent}%). Можно привлекать как наставника.`);
  recs.push(`<b>В целом:</b> средний результат по группе — ${sum.avg_percent}% (${avgScore} из ${maxScore} баллов). ${sum.avg_percent < 70 ? "Уровень группы ниже целевого — планируйте повторение ключевых тем." : "Уровень группы приемлемый, работайте над точечными темами."}`);
  $("#recommendations").innerHTML = recs.map((r, i) =>
    `<div class="rec"><div class="rec-num">${i + 1}</div><div class="rec-body">${r}</div></div>`).join("");
}

function renderResultsAnalysis() {
  if (realResults) {
    renderRealResults(realResults);
    return;
  }
  const test = currentResultsTest();
  const notice = $("#demoNotice");
  const usingFile = $("#demoTestSelect").value === "file";
  const resultsBox = $("#demoResults");

  if (!test) {
    resultsBox.hidden = true;
    notice.hidden = false;
    notice.textContent = "Сначала выберите тест в разделе «Дисциплины и тесты» и проанализируйте его в разделе «Анализ теста», либо выберите встроенный демо-тест из списка.";
    $("#testTitle").textContent = "Анализ результатов";
    $("#testMeta").textContent = "нет данных о выбранном тесте";
    return;
  }

  resultsBox.hidden = false;
  notice.hidden = false;
  notice.textContent = realResults
    ? "Показаны реальные результаты из кабинета onlinetestpad."
    : usingFile
      ? "Показаны синтетические ответы студентов (демо). Нажмите «Загрузить реальные результаты из кабинета»."
      : "Это встроенные демо-данные для примера.";

  const a = analyzeTest(test);
  const disc = usingFile
    ? (fileState.discipline ? fileState.discipline.name : "")
    : (DEMO_DATA.disciplines.find(d => d.tests.some(t => t.id === demoTest.id)) || {}).name || "";
  $("#testTitle").textContent = test.name + " — анализ результатов";
  $("#testMeta").textContent = `${disc} · ${a.test.students.length} студентов · ${a.test.questions.length} вопросов`;

  $("#summaryCards").innerHTML = `
    <div class="card"><div class="k">Студентов</div><div class="v">${a.test.students.length}</div></div>
    <div class="card"><div class="k">Средний результат</div><div class="v">${a.avg}%</div><div class="d">медиана ${a.median}%</div></div>
    <div class="card green"><div class="k">Сдали (≥60%)</div><div class="v">${a.passed}</div><div class="d">не сдали: ${a.failed}</div></div>
    <div class="card ${a.failed > 0 ? "red" : "green"}"><div class="k">Вопросов</div><div class="v">${a.test.questions.length}</div></div>
    <div class="card amber"><div class="k">Сложных вопросов</div><div class="v">${a.perQuestion.filter(q => q.rate < 0.6).length}</div><div class="d">верных &lt; 60%</div></div>`;

  const maxC = Math.max(1, ...a.buckets.map(b => b.count));
  $("#scoreChart").innerHTML = a.buckets.map(b => `
    <div class="col">
      <div class="lbl">${b.count}</div>
      <div class="bar ${b.max <= 40 ? "bad" : b.max <= 60 ? "warn" : ""}" style="height:${Math.max(6, b.count / maxC * 100)}%"></div>
      <div class="lbl">${b.label}</div>
    </div>`).join("");

  const sortedQ = [...a.perQuestion].sort((x, y) => x.rate - y.rate);
  $("#problemQuestions").innerHTML = sortedQ.map(q => {
    const color = colorFor(q.rate);
    return `
    <div class="pq">
      <div class="pq-top">
        <span class="pq-q"><span class="qnum">В${q.idx + 1}</span>${esc(q.text)}<span class="pq-tag">${esc(q.topic)}</span></span>
        <span class="pq-rate" style="color:${color}">${pct(q.rate)}%</span>
      </div>
      <div class="pq-track"><div class="pq-fill" style="width:${pct(q.rate)}%;background:${color}"></div></div>
      ${q.wrong.length ? `<div class="pq-wrong">Ошиблись: ${q.wrong.map(esc).join(", ")}</div>` : '<div class="pq-wrong">Ошибок нет</div>'}
    </div>`;
  }).join("");

  const qCount = a.test.questions.length;
  let table = `<table class="matrix">
    <thead><tr>
      <th>Студент</th>
      ${a.perQuestion.map((q, i) => `<th class="qhead ${q.rate < 0.6 ? "bad-q" : ""}" title="В${i + 1}. ${esc(q.text)} (${esc(q.topic)})">В${i + 1}</th>`).join("")}
      <th>Верно</th><th>%</th>
    </tr></thead><tbody>`;
  a.perStudent.forEach(s => {
    const cls = s.rate < 0.6 ? " class=\"low\"" : "";
    table += `<tr${cls}>
      <td class="stu-name">${esc(s.name)}</td>
      ${s.answers.map(v => `<td class="${v ? "ok" : "bad"}">${v ? "✓" : "✗"}</td>`).join("")}
      <td class="score-cell">${s.correct}/${qCount}</td>
      <td class="score-cell">${pct(s.rate)}%</td>
    </tr>`;
  });
  table += "</tbody></table>";
  $("#matrixTable").innerHTML = table;

  $("#topicsPanel").innerHTML = a.topics.map(t => {
    const color = colorFor(t.rate);
    return `
    <div class="topic">
      <span class="t-name">${esc(t.name)}</span>
      <span class="t-rate" style="color:${color}">${pct(t.rate)}%</span>
      <div class="t-track"><div class="t-fill" style="width:${pct(t.rate)}%;background:${color}"></div></div>
    </div>`;
  }).join("") || '<div class="empty-note">Нет данных</div>';

  $("#repeatsPanel").innerHTML = a.repeats.length ? a.repeats.map(r => {
    const qList = r.questions.map(i => `В${i + 1} — ${esc(a.perQuestion[i].text)}`).join("<br>");
    const stuList = r.students.map(h =>
      `${esc(h.name)} (не ответил на ${h.missed} из ${r.questions.length})`).join("<br>");
    return `<div class="repeat">
      <div class="r-topic">Тема: ${esc(r.topic)}</div>
      <div class="r-q">${qList}</div>
      <div class="r-stu">${stuList}</div>
    </div>`;
  }).join("") : '<div class="empty-note">Повторяющихся ошибок по темам не выявлено — молодец!</div>';

  const recs = [];
  if (a.perQuestion.some(q => q.rate < 0.5)) {
    const worst = a.perQuestion.filter(q => q.rate < 0.5).sort((x, y) => x.rate - y.rate);
    recs.push(`<b>Самые проблемные вопросы:</b> ${worst.map(q => `В${q.idx + 1} «${esc(q.text)}» (${pct(q.rate)}% верных)`).join("; ")}. Стоит разобрать их на занятии и добавить в повторение.`);
  }
  if (a.weakTopics.length) {
    const w = a.weakTopics.slice(0, 3).map(t => `«${esc(t.name)}» (${pct(t.rate)}%)`).join(", ");
    recs.push(`<b>Слабые темы:</b> ${w}. Рекомендуется повторить теорию и дать тренировочные задания именно по этим темам.`);
  }
  if (a.riskGroup.length) {
    recs.push(`<b>Группа риска:</b> ${a.riskGroup.map(esc).join(", ")} — ошибаются в нескольких слабых темах сразу. С ними нужна индивидуальная консультация.`);
  }
  const lag = a.perStudent.filter(s => s.rate < 0.6).map(s => esc(s.name)).join(", ");
  if (lag) recs.push(`<b>Отстающие студенты:</b> ${lag}. Рекомендуется дополнительное задание или повторное прохождение теста после разбора ошибок.`);
  const top = a.perStudent[0];
  if (top) recs.push(`<b>Отличники:</b> ${esc(top.name)} (${pct(top.rate)}%). Можно привлекать как наставников при групповой работе.`);
  recs.push(`<b>В целом:</b> средний результат по группе — ${a.avg}%, сдали ${a.passed} из ${a.test.students.length} (${pct(a.passed / a.test.students.length)}%). ${a.avg < 70 ? "Уровень группы ниже целевого — планируйте повторение ключевых тем." : "Уровень группы приемлемый, работайте над точечными темами."}`);

  $("#recommendations").innerHTML = recs.map((r, i) =>
    `<div class="rec"><div class="rec-num">${i + 1}</div><div class="rec-body">${r}</div></div>`).join("");
}

/* ============================================================
   СОБЫТИЯ И НАВИГАЦИЯ
   ============================================================ */

function switchTo(view) {
  document.querySelectorAll(".nav-item").forEach(b => b.classList.toggle("active", b.dataset.view === view));
  document.querySelectorAll(".view").forEach(v => v.classList.add("hidden"));
  $("#view-" + view).classList.remove("hidden");
}

document.querySelectorAll(".nav-item").forEach(btn => {
  btn.addEventListener("click", () => {
    const v = btn.dataset.view;
    switchTo(v);
    if (v === "analysis") renderResultsAnalysis();
    if (v === "select") { renderFileDisciplines(); renderFileTests(); }
  });
});

$("#disciplineList").addEventListener("click", (e) => {
  const li = e.target.closest("li[data-name]"); if (!li || !fileData) return;
  if (analyzing) { showQaError("Дождитесь завершения анализа текущего теста."); return; }
  fileState.discipline = fileData.disciplines.find(d => d.name === li.dataset.name);
  fileState.test = null;
  renderFileDisciplines(); renderFileTests();
});

$("#testList").addEventListener("click", (e) => {
  const li = e.target.closest("li[data-url]"); if (!li || !fileState.discipline) return;
  if (analyzing) { showQaError("Дождитесь завершения анализа текущего теста."); return; }
  const test = fileState.discipline.tests.find(t => t.url === li.dataset.url);
  if (!test) return;
  fileState.test = test;
  renderFileTests();
  analyzeQuality(test);
});

$("#btnQaRun").addEventListener("click", () => {
  const url = normUrl($("#qaUrl").value);
  if (!url) { showQaError("Вставьте ссылку на тест onlinetestpad.com"); return; }
  analyzeQuality({ url, name: "Тест по ссылке" });
});
$("#qaUrl").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#btnQaRun").click(); });

$("#qaFilter").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-verdict]"); if (!btn) return;
  qaFilter = btn.dataset.verdict;
  document.querySelectorAll("#qaFilter button").forEach(b => b.classList.toggle("active", b === btn));
  renderQaQuestions();
});

$("#demoTestSelect").addEventListener("change", (e) => {
  const id = Number(e.target.value);
  if (e.target.value !== "file") realResults = null;
  for (const d of DEMO_DATA.disciplines)
    for (const t of d.tests)
      if (t.id === id) { demoTest = t; break; }
  renderResultsAnalysis();
});

$("#btnSelectTest").addEventListener("click", () => switchTo("select"));

$("#btnLoadStats").addEventListener("click", loadRealStats);
$("#btnLoadDemo").addEventListener("click", () => {
  realResults = null;
  $("#demoTestSelect").value = "file";
  renderResultsAnalysis();
});

/* --- кабинет onlinetestpad --- */

function setConn(on, email) {
  $("#connBlock").hidden = false;
  const dot = $("#connDot"), txt = $("#connText");
  if (on) {
    dot.className = "dot on";
    txt.textContent = "Кабинет подключён" + (email ? " · " + email : "");
    $("#btnDisconnect").hidden = false;
    $("#btnConnect").textContent = "Кабинет подключён";
  } else {
    dot.className = "dot off";
    txt.textContent = "Не подключено";
    $("#btnDisconnect").hidden = true;
    $("#btnConnect").textContent = "Подключить кабинет";
  }
}

async function refreshStatus() {
  try {
    const r = await fetch("/api/status");
    const j = await r.json();
    setConn(!!j.connected, j.email);
  } catch (e) {
    setConn(false, null);
  }
}

$("#btnConnect").addEventListener("click", () => {
  if (document.querySelector('#connDot').classList.contains('on')) {
    switchTo("select");
  } else {
    switchTo("login");
  }
});

$("#btnDisconnect").addEventListener("click", async () => {
  try { await fetch("/api/logout", { method: "POST" }); } catch (e) {}
  setConn(false, null);
  realResults = null;
  $("#demoTestSelect").value = "file";
  renderResultsAnalysis();
});

$("#btnTogglePass").addEventListener("click", () => {
  const input = $("#loginPassword");
  const btn = $("#btnTogglePass");
  const show = input.type === "password";
  input.type = show ? "text" : "password";
  btn.textContent = show ? "🙈" : "👁";
  btn.setAttribute("aria-pressed", String(show));
});

$("#loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = $("#loginEmail").value.trim();
  const password = $("#loginPassword").value;
  const errEl = $("#loginError");
  errEl.hidden = true;
  const btn = $("#loginSubmit");
  btn.disabled = true;
  btn.textContent = "Вход…";
  try {
    const r = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    const j = await r.json();
    if (!j.ok) {
      errEl.textContent = j.error || "Ошибка входа.";
      errEl.hidden = false;
      return;
    }
    setConn(true, j.email);
    switchTo("select");
  } catch (err) {
    errEl.textContent = "Сервер не отвечает: " + err.message;
    errEl.hidden = false;
  } finally {
    btn.disabled = false;
    btn.textContent = "Войти";
  }
});

/* фильтр по студенту (демо) */
$("#studentFilter").addEventListener("input", (e) => {
  const q = e.target.value.trim().toLowerCase();
  document.querySelectorAll("#matrixTable tbody tr").forEach(tr => {
    tr.style.display = tr.querySelector(".stu-name").textContent.toLowerCase().includes(q) ? "" : "none";
  });
});

$("#btnExport").addEventListener("click", () => window.print());

/* инициализация */
renderDemoSelect();
refreshStatus();
loadTestsFile();
switchTo("select");