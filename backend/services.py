from backend.database import get_connection
from backend.llm_model.llm import ask_database

import pickle
import pandas as pd
import numpy as np
import os
from fastapi import HTTPException

# ---------- CRUD SERVICES ----------

def add_patient_service(patient):
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
            patient.symptoms
        ))
        conn.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    finally:
        conn.close()

    return {"message": "Patient added successfully"}


def get_patient_service(patient_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")

    return dict(row)


def get_all_patients_service():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def update_patient_service(patient_id: str, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")

    fields = []
    values = []

    for k, v in data.dict(exclude_unset=True).items():
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


def delete_patient_service(patient_id: str):
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


def patient_profile_service(patient_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")

    return dict(row)


# ---------- LLM SERVICE ----------

def chat_db_service(question: str):
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


def predict_service(symptoms: list):

    if not symptoms:
        raise HTTPException(status_code=400, detail="Symptoms required")

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
