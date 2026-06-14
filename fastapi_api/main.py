#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import uvicorn
import os


MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'spam_detector', 'model_spam.pkl')

try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
except FileNotFoundError:
    print(f"⚠️  Modelul nu a fost găsit la {MODEL_PATH}. Rulează întâi spam_detector.py")
    model = None
    model_loaded = False


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class PredictionOutput(BaseModel):
    text: str
    este_spam: bool
    eticheta: str
    siguranta_spam: float


app = FastAPI(
    title="Spam Detector API",
    description="API care primește un text și returnează probabilitatea de a fi spam.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "api": "Spam Detector API", "versiune": "1.0.0"}


@app.get("/health")
def health():
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Modelul nu este încărcat")
    return {"status": "healthy", "model_incarcat": True}


@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: TextInput):
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Modelul nu este disponibil. Rulează întâi spam_detector.py")

    text = input_data.text

    try:
        probabilitati = model.predict_proba([text])[0]
        eticheta_cifra = model.predict([text])[0]

        return PredictionOutput(
            text=text,
            este_spam=bool(eticheta_cifra == 1),
            eticheta="spam" if eticheta_cifra == 1 else "ham",
            siguranta_spam=round(float(probabilitati[1]), 4),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare la predicție: {str(e)}")


if __name__ == '__main__':
    if not model_loaded:
        print("❌ Rulează întâi: python3 ../spam_detector/spam_detector.py")
        exit(1)

    uvicorn.run(app, host="0.0.0.0", port=8000)
