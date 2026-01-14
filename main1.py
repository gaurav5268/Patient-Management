import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pickle

from Backend.llm_model.llm import ask_database

result = ask_database("Show patients from Delhi")



app = FastAPI()

# ---------------- Static + Templates ----------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Load ML Model ----------------
with open("model/disease_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

with open("model/symptom_list.pkl", "rb") as f:
    symptom_list = pickle.load(f)

print("Model loaded, symptoms:", len(symptom_list))

# ---------------- Database ----------------
conn = sqlite3.connect("data/mydatabase.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    city TEXT,
    height REAL,
    weight REAL,
    diagnosis TEXT,
    status TEXT,
    mobile TEXT,
    symptoms TEXT
)
""")
conn.commit()

# ---------------- Schemas ----------------
class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient( example - 001)")]
    name :Annotated[str, Field(..., description = "Name of the patient( example - Guarav Chauhan)")]
    age : Annotated[int, Field(..., gt =0,  lt = 120, description = "Age of the patient( example - 22)")]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description = "ID of the patient( example - male)")]
    city : Annotated[str, Field(..., description = "Hometown/Receding city of the patient( example - Varanasi)")]
    height : Annotated[float, Field(..., gt =0,  description = "Height of the patient in cm ( example - 172 cm")]
    weight : Annotated[float, Field(..., gt =0,  description = "Weigth of the patient in kg ( example - 58 kg")]
    diagnosis : Annotated[str, Field(..., description = "Diagnosis of the patient")]
    status: Annotated[Literal['ongoing', 'over'], Field(..., description="Treatment status")]
    mobile: Annotated[str, Field(..., min_length=10, max_length=10, description="10 digit mobile number")]
    symptoms: Annotated[str, Field(..., description="Selected symptoms (comma separated)")]

    @computed_field
    @property
    def BMI(self) -> float:
        h = self.height / 100
        return round(self.weight / (h ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.BMI < 18.5:
            return "Underweight"
        elif self.BMI < 25:
            return "Normal"
        else:
            return "Overweight"


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['male', 'female', 'others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    diagnosis: Optional[str] = None
    status: Optional[Literal['ongoing', 'over']] = None
    mobile: Optional[str] = Field(default=None, min_length=10, max_length=10)
    symptoms: Optional[str] = None


class SymptomRequest(BaseModel):
    symptoms: list[str]

# ---------------- Pages ----------------
@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------- CRUD ----------------
@app.post("/patients")
def add_patient(patient: Patient):
    try:
        cursor.execute("""
        INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient.id,
            patient.name,
            patient.age,
            patient.gender,
            patient.city,
            patient.height,
            patient.weight,
            patient.diagnosis,
            patient.status,
            patient.mobile,
            patient.symptoms
        ))
        conn.commit()
        return {"message": "Patient added successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Patient ID already exists")


@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")

    return Patient(
        id=row[0],
        name=row[1],
        age=row[2],
        gender=row[3],
        city=row[4],
        height=row[5],
        weight=row[6],
        diagnosis=row[7],
        status=row[8],
        mobile=row[9],
        symptoms=row[10]
    )


@app.get("/patients")
def get_all_patients():
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()

    return [
        Patient(
            id=r[0],
            name=r[1],
            age=r[2],
            gender=r[3],
            city=r[4],
            height=r[5],
            weight=r[6],
            diagnosis=r[7],
            status=r[8],
            mobile=r[9],
            symptoms=r[10]
        )
        for r in rows
    ]


@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, data: PatientUpdate):
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Patient not found")

    fields = []
    values = []

    for key, value in data.dict(exclude_unset=True).items():
        fields.append(f"{key} = ?")
        values.append(value)

    values.append(patient_id)

    query = f"UPDATE patients SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(values))
    conn.commit()

    return {"message": "Patient updated successfully"}


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Patient not found")

    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()

    return {"message": "Patient deleted successfully"}

# ---------------- Extra APIs ----------------
@app.get("/symptoms")
def get_symptoms():
    return {"symptoms": symptom_list}

# ---------------- Prediction ----------------
def clean_symptom(s):
    return s.strip().lower().replace(" ", "_").replace("__", "_")


@app.post("/predict")
def predict(req: SymptomRequest):

    input_data = pd.DataFrame(0, index=[0], columns=symptom_list)

    for symptom in req.symptoms:
        s = clean_symptom(symptom)
        if s in input_data.columns:
            input_data.at[0, s] = 1
        else:
            return {"error": f"Symptom '{symptom}' not recognized"}

    prediction = model.predict(input_data)[0]
    disease = label_encoder.inverse_transform([prediction])[0]

    probs = model.predict_proba(input_data)[0]
    confidence = float(np.max(probs))

    return {
        "predicted_disease": disease,
        "confidence": round(confidence * 100, 2)
    }
