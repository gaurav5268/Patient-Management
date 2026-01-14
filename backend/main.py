from fastapi import FastAPI, HTTPException, Request
from typing import List

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.database import get_connection, init_db
from backend.models import Patient, PatientUpdate
from backend.llm_model.llm import ask_database
import pickle
import pandas as pd
import numpy as np
import os



app = FastAPI(title="Patient Management System")

# Initialize database
init_db()

# ---------------- TEMPLATE + STATIC ----------------
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- PAGE ROUTES ----------------

@app.get("/")
def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


@app.get("/update")
def update_page(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})


@app.get("/view")
def view_page(request: Request):
    return templates.TemplateResponse("view.html", {"request": request})


# ---------------- API ROUTES ----------------

@app.post("/patients")
def add_patient(patient: Patient):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient.id,
            patient.name,
            patient.age,
            patient.gender,
            patient.city,
            patient.height,
            patient.weight,
            patient.status,
            patient.mobile,
            ",".join(patient.symptoms)
        ))
        conn.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    finally:
        conn.close()

    return {"message": "Patient added successfully"}


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")

    return dict(row)


@app.get("/patients")
def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, data: PatientUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")

    fields = []
    values = []

    for k, v in data.dict(exclude_unset=True).items():
        if k == "symptoms":
            v = ",".join(v)
        fields.append(f"{k}=?")
        values.append(v)

    values.append(patient_id)

    cursor.execute(
        f"UPDATE patients SET {', '.join(fields)} WHERE id=?",
        values
    )

    conn.commit()
    conn.close()

    return {"message": "Patient updated successfully"}


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")

    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()

    return {"message": "Patient deleted successfully"}


@app.get("/profile/{patient_id}")
def patient_profile(request: Request, patient_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient = dict(row)

    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "patient": patient}
    )
@app.get("/assistant")
def assistant_page(request: Request):
    return templates.TemplateResponse("assistant.html", {"request": request})

@app.post("/chat-db")
def chat_db(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question required")

    return ask_database(question)


# ---------- ML MODEL LOADING ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, "ml_model")

with open(os.path.join(ML_DIR, "disease_model.pkl"), "rb") as f:
    ml_model = pickle.load(f)

with open(os.path.join(ML_DIR, "label_encoder.pkl"), "rb") as f:
    label_encoder = pickle.load(f)

with open(os.path.join(ML_DIR, "symptom_list.pkl"), "rb") as f:
    symptom_list = pickle.load(f)

@app.post("/predict")
def predict(payload: dict):
    symptoms = payload.get("symptoms", [])

    if not symptoms:
        raise HTTPException(status_code=400, detail="Symptoms required")

    # Build input
    input_data = pd.DataFrame(0, index=[0], columns=symptom_list)

    for s in symptoms:
        s = s.strip().lower().replace(" ", "_")
        if s in input_data.columns:
            input_data.at[0, s] = 1

    pred = ml_model.predict(input_data)[0]
    disease = label_encoder.inverse_transform([pred])[0]

    prob = float(np.max(ml_model.predict_proba(input_data)))

    return {
        "predicted_disease": disease,
        "confidence": round(prob * 100, 2)
    }
