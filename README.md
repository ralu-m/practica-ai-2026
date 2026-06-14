# Practică Inteligență Artificială 2026

**Studentă:** Moisuc Raluca-Elena  
**Facultatea:** Automatică și Calculatoare, Iași — Anul 3

## Proiecte

### 1. Spam Detector — Clasificator Binar
- Antrenare model Naive Bayes pe text (Scikit-learn)
- Evaluare: acuratețe, precizie, recall, F1-score
- Salvare model cu joblib

### 2. FastAPI — Deployment model
- API REST pentru predicții spam/ham
- Endpoint-uri: GET `/`, GET `/health`, POST `/predict`
- Documentație Swagger automată la `/docs`

### 3. Linux Backup & Monitorizare
- Backup automat + rotație (păstrează ultimele 7)
- Monitorizare CPU, RAM, disc
- Alertă la depășirea pragurilor

## Rulare

```bash
pip install -r requirements.txt
cd spam_detector && python3 spam_detector.py
cd ../fastapi_api && python3 main.py
```
