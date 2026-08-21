"""TestPad Analyzer — локальный веб-сервер.

Маршруты:
  GET  /                    — интерфейс (дашборд)
  POST /api/login           — вход в onlinetestpad (логин/пароль из тела запроса)
  POST /api/logout          — выход и закрытие браузерной сессии
  GET  /api/status          — статус подключения
  GET  /api/disciplines     — список папок (дисциплин) и тестов из личного кабинета
  GET  /api/diagnostics     — диагностика парсера (текущая страница, образцы ссылок)

Пароль нигде не сохраняется и не логируется — используется только
для входа в Playwright-сессию и живёт в памяти процесса.
"""

from flask import Flask, request, jsonify, send_from_directory
import os

from otp_client import OTPClient, OTPError
import analyzer
import tests_loader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/")

# Единственный клиент на процесс. Flask запускаем в одном потоке
# (threaded=False), т.к. Playwright-sync привязан к потоку.
client = OTPClient()


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.post("/api/login")
def api_login():
    body = request.get_json(silent=True) or {}
    email = (body.get("email") or "").strip()
    password = body.get("password") or ""
    if not email or not password:
        return jsonify({"ok": False, "error": "Укажите e-mail и пароль."}), 400
    try:
        client.login(email, password)
        return jsonify({"ok": True, "email": email})
    except OTPError as e:
        return jsonify({"ok": False, "error": str(e)}), 401
    except Exception as e:
        return jsonify({"ok": False, "error": f"Внутренняя ошибка: {e}"}), 500


@app.post("/api/logout")
def api_logout():
    client._clear_state()  # удаляем сохранённую сессию (выход)
    client.close()
    return jsonify({"ok": True})


@app.get("/api/status")
def api_status():
    return jsonify({"connected": client.connected, "email": client.email})


@app.get("/api/disciplines")
def api_disciplines():
    try:
        disciplines, raw = client.fetch_disciplines()
        return jsonify({"ok": True, "disciplines": disciplines, "raw": raw})
    except OTPError as e:
        return jsonify({"ok": False, "error": str(e)}), 401
    except Exception as e:
        return jsonify({"ok": False, "error": f"Внутренняя ошибка: {e}"}), 500


@app.get("/api/diagnostics")
def api_diagnostics():
    try:
        return jsonify({"ok": True, **client.diagnostics()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.get("/api/tests-file")
def api_tests_file():
    """Список папок и тестов: из Excel-файла (автообновление) или из data/tests.json."""
    try:
        return jsonify({"ok": True, **tests_loader.load_tests()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.post("/api/analyze")
def api_analyze():
    """Анализ качества теста по его ссылке (обход теста + эвристики)."""
    body = request.get_json(silent=True) or {}
    url = (body.get("url") or "").strip()
    if not url:
        return jsonify({"ok": False, "error": "Не указана ссылка на тест."}), 400
    try:
        questions_data = client.fetch_test_questions(url)
        analysis = analyzer.analyze_test(questions_data)
        return jsonify({"ok": True, **analysis})
    except OTPError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": f"Внутренняя ошибка: {e}"}), 500


@app.post("/api/statistics")
def api_statistics():
    """Таблица ответов студентов по тесту (нужен вход в кабинет)."""
    body = request.get_json(silent=True) or {}
    url = (body.get("url") or "").strip()
    if not url:
        return jsonify({"ok": False, "error": "Не указана ссылка на тест."}), 400
    sub = (body.get("sub") or "answers").strip()
    name = (body.get("name") or "").strip()
    try:
        data = client.fetch_test_statistics(url, sub=sub, name=name)
        return jsonify({"ok": True, **data})
    except OTPError as e:
        return jsonify({"ok": False, "error": str(e)}), 401
    except Exception as e:
        return jsonify({"ok": False, "error": f"Внутренняя ошибка: {e}"}), 500


if __name__ == "__main__":
    # threaded=False: Playwright-sync должен работать в одном потоке
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=False)