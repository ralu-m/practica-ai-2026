#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import os


def genereaza_date():
    ham = [
        "Salut, ce faci?",
        "Hai la bere diseară?",
        "Întâlnirea e mâine la 10",
        "Factura a fost plătită",
        "Mulțumesc pentru ajutor",
        "Am primit pachetul, e ok",
        "Te sun mai târziu",
        "Proiectul e gata, verifică-l",
        "Ce mai faci?",
        "Cum a fost la curs?",
        "Trebuie să predau tema mâine",
        "Mă întâlnesc cu echipa la prânz",
    ]
    spam = [
        "Câștigă 10.000 Lei acum!",
        "Ofertă limitată, doar azi!",
        "Dă click aici pentru premiul tău",
        "Ai fost selectat câștigător",
        "Investește și câștigă rapid",
        "Cumpără ieftin, vinde scump",
        "Numărătoare inversă: oferta expiră!",
        "Supliment miraculos, comandă acum",
        "Felicitări! Ai câștigat un iPhone",
        "Ofertă exclusivă pentru tine",
        "Ultima șansă! Reducere 50%",
        "Câștigă bani fără efort",
    ]

    texte = ham + spam
    etichete = [0] * len(ham) + [1] * len(spam)

    df = pd.DataFrame({'text': texte, 'label': etichete})
    return df


def antreneaza_model(df):
    X = df['text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    print("🔄 Antrenare model în curs...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("\n" + "=" * 50)
    print("📊 EVALUARE MODEL")
    print("=" * 50)
    print(f"  Accuracy:           {accuracy_score(y_test, y_pred):.2%}")
    print(f"  Precision:          {precision_score(y_test, y_pred):.2%}")
    print(f"  Recall:             {recall_score(y_test, y_pred):.2%}")
    print(f"  F1-score:           {f1_score(y_test, y_pred):.2%}")
    print()
    print("📋 Matrice de confuzie:")
    print(confusion_matrix(y_test, y_pred))
    print()
    print("📋 Raport detaliat:")
    print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))
    print("=" * 50)

    return pipeline


def salveaza_model(pipeline, cale=os.path.join(os.path.dirname(__file__), 'model_spam.pkl')):
    joblib.dump(pipeline, cale)
    marime = os.path.getsize(cale)
    print(f"✅ Model salvat: {cale} ({marime} bytes)")


def incarca_si_testeaza(cale=os.path.join(os.path.dirname(__file__), 'model_spam.pkl')):
    model = joblib.load(cale)
    print(f"\n✅ Model încărcat din: {cale}")

    exemple = [
        "Salut, ne vedem la cafea?",
        "Câștigă 1 milion de euro acum!",
        "Raportul e în attachment",
        "Ofertă exclusivă doar pentru tine",
        "Mâine avem întâlnire de proiect",
        "Ultima șansă! Reducere 50% la toate produsele",
    ]

    print("\n" + "=" * 50)
    print("🔍 TESTARE PE EXEMPLE NOI")
    print("=" * 50)
    for text in exemple:
        prob = model.predict_proba([text])[0]
        eticheta = model.predict([text])[0]
        tip = "🚫 SPAM" if eticheta == 1 else "✅ HAM"
        siguranta = prob[1] * 100
        print(f"  '{text}'")
        print(f"  → {tip}  (probabilitate spam: {siguranta:.1f}%)")
        print()


if __name__ == '__main__':
    print("=" * 50)
    print("🧪 PROIECT 1: SPAM DETECTOR")
    print("   Clasificator Binar cu Scikit-learn")
    print("=" * 50)

    df = genereaza_date()
    print(f"\n📝 Date de antrenare: {len(df)} mesaje")
    print()

    model = antreneaza_model(df)
    salveaza_model(model)
    incarca_si_testeaza()
