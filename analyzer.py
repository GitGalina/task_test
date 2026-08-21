"""Анализ качества теста по собранным вопросам (локальные эвристики).

Оценивает по каждому вопросу:
  - корректность формулировки и вариантов
  - профессионализм (стиль, эмодзи, слабые формулировки, «все вышеперечисленное»)
  - уровень сложности (оценка 1-5)
  - соответствие заявленной теме (по ключевым словам из названия теста)

И формирует рекомендации: что упростить, усложнить, добавить.
"""

import re
from collections import Counter

TYPE_LABELS = {
    "single": "Одиночный выбор",
    "multiple": "Множественный выбор",
    "text": "Развёрнутый ответ",
    "select": "Выбор из списка",
    "input": "Ввод ответа",
    "other": "Соответствие / последовательность / др.",
}

# фразы, которые плохо смотрятся в вариантах ответа
WEAK_OPTION_PHRASES = [
    "все вышеперечисленное", "ничего из перечисленного",
    "все варианты верны", "все ответы верны", "нет правильного ответа",
]

STOPWORDS = {
    "и", "в", "на", "по", "для", "с", "из", "как", "что", "это", "тест",
    "тестирование", "проверка", "контроль", "итоговый", "входной", "срез",
    "зачёт", "экзамен", "вариант", "работа", "класс", "номер", "задания",
    "такое", "можно", "нужно", "будет", "если", "есть", "какой", "какая",
    "какие", "какие", "который", "которые", "про", "при", "от", "до", "между",
}

EMOJI_RE = re.compile(
    r"[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u2B50\u274C\u2705\u2764\u2694]"
)
CODE_RE = re.compile(r"[{}()\[\];]|=>|class\s|public|private|protected|static|new\s")
Q_MARK_RE = re.compile(r"[?？]")
NUM_RE = re.compile(r"\d")

# тезаурус: тема -> характерные понятия (основы для проверки соответствия вопросов теме)
TOPIC_CONCEPTS = {
    "ооп": [
        "ооп", "объект", "класс", "наследовани", "полиморфизм", "инкапсуляци",
        "абстракци", "интерфейс", "переопредел", "виртуальн", "конструктор",
        "свойств", "метод", "экземпляр", "is-a", "has-a",
    ],
    "программирован": [
        "программ", "алгоритм", "переменн", "цикл", "услови", "массив", "c#",
        "python", "java", "функци",
    ],
    "математик": [
        "числ", "уравнен", "функци", "производн", "интеграл", "корень",
        "сумм", "значен", "формул", "выражен",
    ],
}


def _norm(s):
    return " ".join(s.lower().split())


def topic_keywords(title):
    """Ключевые слова темы из названия теста + расширения аббревиатур."""
    words = re.findall(r"[а-яёa-z0-9]{3,}", (title or "").lower())
    kws = [w for w in words if w not in STOPWORDS and not w.isdigit()]
    extra = []
    for w in kws:
        if w == "ооп":
            extra += ["ооп", "объект", "объектно"]
        if w.startswith("оаип"):
            extra += ["алгоритм", "программирован"]
        if w in ("информатика",):
            extra += ["программ", "компьютер", "данн"]
        if w in ("математика",):
            extra += ["числ", "уравнен", "функци"]
    return list(dict.fromkeys(kws + extra))


def _dominant_words(questions):
    """Слова, встречающиеся в нескольких вопросах теста (стержень темы)."""
    cnt = Counter()
    for q in questions:
        words = set(re.findall(r"[а-яёa-z]{5,}", (q.get("qtext") or "").lower()))
        for w in words:
            if w not in STOPWORDS:
                cnt[w] += 1
    n = len(questions)
    min_c = 2 if n < 8 else max(2, int(n * 0.25))
    return [w for w, c in cnt.most_common(15) if c >= min_c]


def _detect_themes(title, dominant):
    """Какие темы из тезауруса упоминаются в названии теста или его вопросах."""
    blob = " ".join([(title or "").lower()] + list(dominant))
    return [key for key in TOPIC_CONCEPTS if key in blob]


def _q_stems(text):
    return {w[:5] for w in re.findall(r"[а-яёa-z]{4,}", (text or "").lower())
            if w not in STOPWORDS}


def _difficulty(q):
    score = 1
    text = q.get("qtext", "")
    opts = q.get("options", [])
    if len(text) > 280:
        score += 1
    if CODE_RE.search(text) or any(CODE_RE.search(o.get("text", "")) for o in opts):
        score += 1
    if q.get("qtype") in ("multiple", "text", "other"):
        score += 1
    avg_opt = sum(len(o.get("text", "")) for o in opts) / max(1, len(opts))
    if avg_opt > 90:
        score += 1
    if len(opts) > 5:
        score += 1
    return max(1, min(5, score))


def analyze_question(q, idx, topic_terms):
    text = (q.get("qtext") or "").strip()
    opts = q.get("options", [])
    qtype = q.get("qtype", "other")
    issues = []  # {level: warn|alert, text}

    # --- корректность ---
    if len(text) < 10:
        issues.append({"level": "alert", "text": "Очень короткая формулировка вопроса."})
    if len(text) < 25:
        issues.append({"level": "warn", "text": "Короткая формулировка — возможно, вопрос слишком простой или неполный."})
    if not Q_MARK_RE.search(text) and qtype in ("single", "multiple", "select"):
        issues.append({"level": "warn", "text": "Формулировка не заканчивается знаком вопроса."})

    # --- профессионализм ---
    if EMOJI_RE.search(text):
        issues.append({"level": "alert", "text": "В тексте вопроса есть эмодзи — для учебного теста это непрофессионально."})
    for o in opts:
        if EMOJI_RE.search(o.get("text", "")):
            issues.append({"level": "warn", "text": "В одном из вариантов есть эмодзи."})
            break
    norm_opts = [_norm(o.get("text", "")) for o in opts]
    if len(norm_opts) != len(set(norm_opts)):
        issues.append({"level": "alert", "text": "Варианты ответа повторяются (дубли)."})
    for phr in WEAK_OPTION_PHRASES:
        for o in norm_opts:
            if phr in o:
                issues.append({"level": "warn", "text": f"Вариант содержит формулировку «{phr}» — обычно снижает качество теста."})
                break

    # угадывание по длине варианта
    if len(opts) >= 2:
        lens = [len(o.get("text", "")) for o in opts]
        maxl, minl = max(lens), min(lens)
        if minl > 0 and maxl / minl > 4 and qtype == "single":
            issues.append({"level": "warn", "text": "Варианты сильно различаются по длине — правильный ответ легко угадать."})
        if maxl > 0 and maxl / max(1, min(lens or [1])) > 4 and qtype in ("single",):
            pass

    if len(opts) < 2:
        issues.append({"level": "warn", "text": "Менее 2 вариантов ответа."})
    elif len(opts) > 8:
        issues.append({"level": "warn", "text": f"Слишком много вариантов ({len(opts)})."})

    # --- соответствие теме ---
    if topic_terms:
        low = text.lower()
        stems = _q_stems(text)
        matched = [t for t in topic_terms
                   if t in low or t[:5] in stems]
        if not matched:
            issues.append({"level": "warn", "text": "Вопрос не связан с темой теста (не встречается ни одно ключевое понятие)."})

    difficulty = _difficulty(q)
    return {
        "idx": idx,
        "qid": q.get("qid", ""),
        "qtype": qtype,
        "qtype_label": TYPE_LABELS.get(qtype, qtype),
        "text": text,
        "options": [{"type": o.get("type"), "text": o.get("text")} for o in opts],
        "issues": issues,
        "difficulty": difficulty,
        "verdict": "ok" if not issues else ("warn" if all(i["level"] == "warn" for i in issues) else "alert"),
    }


def analyze_test(test):
    title = test.get("title", "")
    url = test.get("url", "")
    questions = test.get("questions", [])
    kws = topic_keywords(title)
    dominant = _dominant_words(questions)
    themes = _detect_themes(title, dominant)
    concepts = [c for t in themes for c in TOPIC_CONCEPTS[t]]
    topic_terms = list(dict.fromkeys(kws + dominant + concepts))

    per_q = [analyze_question(q, i, topic_terms) for i, q in enumerate(questions)]
    per_q.sort(key=lambda q: int(q["qid"]) if str(q["qid"]).isdigit() else 0)
    for i, q in enumerate(per_q):
        q["idx"] = i
    type_counts = Counter(q["qtype_label"] for q in per_q)
    all_issues = [i for q in per_q for i in q["issues"]]
    alerts = [i for i in all_issues if i["level"] == "alert"]
    warns = [i for i in all_issues if i["level"] == "warn"]
    diffs = [q["difficulty"] for q in per_q]
    avg_diff = round(sum(diffs) / len(diffs), 1) if diffs else 0

    recs = build_recommendations(title, per_q, type_counts, topic_terms)

    return {
        "title": title,
        "url": url,
        "count": len(per_q),
        "keywords": kws,
        "themes": themes,
        "dominant_words": dominant,
        "topic_terms": topic_terms,
        "type_counts": dict(type_counts),
        "avg_difficulty": avg_diff,
        "difficulty_dist": dict(Counter(diffs)),
        "issues_total": {"alert": len(alerts), "warn": len(warns)},
        "questions": per_q,
        "recommendations": recs,
        "score": quality_score(len(alerts), len(warns), len(per_q)),
    }


def quality_score(alerts, warns, count):
    """Грубая оценка качества теста 0-100."""
    if not count:
        return 0
    base = 100
    base -= alerts * 10
    base -= warns * 4
    return max(0, min(100, base))


def build_recommendations(title, per_q, type_counts, topic_terms):
    recs = []
    count = len(per_q)

    if not count:
        return recs

    # --- упростить ---
    hard = [q for q in per_q if q["difficulty"] >= 4]
    if hard and len(hard) / count >= 0.4:
        recs.append({
            "kind": "simplify",
            "text": f"Много вопросов высокой сложности ({len(hard)} из {count}). Упростите: разбейте длинные формулировки, сократите варианты, добавьте вопросы с одиночным выбором по базовым понятиям.",
        })
    for q in hard[:3]:
        recs.append({
            "kind": "simplify",
            "text": f"Вопрос {q['idx'] + 1}: высокая сложность (уровень {q['difficulty']}). При необходимости упростите формулировку или разбейте на подвопросы.",
        })

    # --- усложнить ---
    easy = [q for q in per_q if q["difficulty"] <= 2]
    if easy and len(easy) / count >= 0.5:
        recs.append({
            "kind": "complicate",
            "text": f"Большинство вопросов простые (уровень ≤ 2). Усложните: добавьте вопросы с кодом, множественным выбором и развёрнутым ответом.",
        })

    # --- добавить ---
    if not type_counts.get("Множественный выбор"):
        recs.append({"kind": "add", "text": "Добавьте вопросы с множественным выбором — они проверяют полноту знаний."})
    if not type_counts.get("Развёрнутый ответ") and not type_counts.get("Ввод ответа"):
        recs.append({"kind": "add", "text": "Добавьте вопросы с вводом текста/числа — сложно угадать, проверяют точность знаний."})
    if not type_counts.get("Соответствие / последовательность / др."):
        recs.append({"kind": "add", "text": "Добавьте вопросы на соответствие или последовательность — развивают системное мышление."})

    # --- тема ---
    off = [q for q in per_q if any(i["level"] == "warn" and "не связан" in i["text"] for i in q["issues"])]
    if topic_terms and len(off) / count >= 0.3:
        recs.append({
            "kind": "topic",
            "text": f"{len(off)} из {count} вопросов не связаны с темой теста. Ключевые понятия темы: «{', '.join(topic_terms[:6])}». Проверьте, не попали ли вопросы из других тем.",
        })

    # --- профессионализм ---
    emoji_q = [q for q in per_q if any("эмодзи" in i["text"] for i in q["issues"])]
    if emoji_q:
        recs.append({"kind": "professional", "text": f"Уберите эмодзи из {len(emoji_q)} вопросов — это снижает профессиональный вид теста."})

    # --- общий вывод ---
    types_txt = ", ".join(f"{k}: {v}" for k, v in type_counts.items())
    recs.append({
        "kind": "general",
        "text": f"В тесте {count} вопросов ({types_txt}). Средний уровень сложности — {round(sum(q['difficulty'] for q in per_q) / count, 1)} из 5.",
    })

    return recs