"""Загрузка списка тестов из Excel-файла в data/tests.json.

Excel: столбцы «папка» / «название дисциплины» / «тест название» / «ссылка».
Папка и дисциплина заполнены только в первой строке группы — переносятся ниже.

Можно запускать вручную:  python update_tests.py
Либо /api/tests-file сам обновит JSON, если Excel новее.
"""

import json
import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "СПИСОК тестов TestPad.xlsx")
JSON_FILE = os.path.join(BASE_DIR, "data", "tests.json")

FOLDER = 0
DISCIPLINE = 1
TEST_NAME = 2
URL = 3


def parse_excel(path):
    xl = pd.ExcelFile(path)
    df = xl.parse(xl.sheet_names[0], header=None, dtype=str)

    disciplines = []
    cur = None  # текущая группа {name, folder, tests}
    for _, row in df.iloc[1:].iterrows():  # 1-я строка — заголовок
        folder = _clean(row.iloc[FOLDER])
        disc = _clean(row.iloc[DISCIPLINE])
        name = _clean(row.iloc[TEST_NAME])
        url = _clean(row.iloc[URL])
        if not name or not url:
            continue
        if folder or disc:
            if not disc:
                disc = folder
            cur = {"name": disc, "folder": folder, "tests": []}
            disciplines.append(cur)
        if cur is None:
            continue
        cur["tests"].append({"name": name, "url": url})

    # убрать пустые группы
    return [d for d in disciplines if d["tests"]]


def _clean(v):
    if v is None:
        return ""
    s = str(v).strip()
    if s.lower() in ("nan", "none"):
        return ""
    return s


def load_tests(excel_path=None, json_path=None):
    excel_path = excel_path or EXCEL_FILE
    json_path = json_path or JSON_FILE
    payload = None
    try:
        if os.path.exists(excel_path):
            payload = {"disciplines": parse_excel(excel_path)}
    except Exception:
        payload = None

    if payload is not None:
        # обновить кэш JSON
        try:
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return payload

    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    data = load_tests()
    for d in data["disciplines"]:
        print(f"{d['folder'] or '-':5} {d['name']} — {len(d['tests'])} тестов")
    print(f"\nВсего дисциплин: {len(data['disciplines'])}, тестов: "
          f"{sum(len(d['tests']) for d in data['disciplines'])}")
    print("OK ->", JSON_FILE)