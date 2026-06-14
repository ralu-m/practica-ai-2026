#!/usr/bin/env python3
import requests

BASE_URL = "http://localhost:8000"


def testeaza():
    print("=" * 50)
    print("🔍 TESTARE API SPAM DETECTOR")
    print("=" * 50)

    print("\n1️⃣  GET /")
    r = requests.get(f"{BASE_URL}/")
    print(f"   Status: {r.status_code}")
    print(f"   Răspuns: {r.json()}")

    print("\n2️⃣  GET /health")
    r = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {r.status_code}")
    print(f"   Răspuns: {r.json()}")

    print("\n3️⃣  POST /predict")
    exemple = [
        "Salut, ce faci?",
        "Câștigă 1 milion de euro!",
        "Mâine avem laborator la 10",
        "Ofertă limitată doar azi!",
    ]
    for text in exemple:
        r = requests.post(f"{BASE_URL}/predict", json={"text": text})
        rezultat = r.json()
        print(f"\n   📝 '{text}'")
        print(f"   → {rezultat['eticheta'].upper()} (siguranță: {rezultat['siguranta_spam']:.1%})")

    print("\n" + "=" * 50)
    print("✅ Testare completă!")
    print("=" * 50)


if __name__ == '__main__':
    testeaza()
