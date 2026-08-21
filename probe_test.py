"""Временный скрипт: тест обходчика вопросов."""
from otp_client import OTPClient

c = OTPClient()
try:
    res = c.fetch_test_questions("https://onlinetestpad.com/6qzasjwq5ctze")
    print("TITLE:", res["title"])
    print("COUNT:", res["count"])
    for i, q in enumerate(res["questions"], 1):
        print(f"\n--- Q{i} [{q['qtype']}] id={q['qid']} ---")
        print(q["qtext"][:120].replace("\n", " / "))
        for o in q["options"]:
            print(f"   ({o['type']}) {o['text'][:80].replace(chr(10), ' / ')}")
        if q["extraInputs"]:
            print("   extra:", q["extraInputs"])
finally:
    c.close()