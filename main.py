from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import sqlite3

app = FastAPI()

conn = sqlite3.connect("mydatabase.db", check_same_thread=False)
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
    mobile TEXT
)
""")
conn.commit()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient( example - 001)")]
    name :Annotated[str, Field(..., description = "Name of the patient( example - Guarav Chauhan)")]
    age : Annotated[int, Field(..., gt =0,  lt = 120, description = "Age of the patient( example - 22)")]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description = "ID of the patient( example - male)")]
    city : Annotated[str, Field(..., description = "Hometown/Receding city of the patient( example - Varanasi)")]
    height : Annotated[float, Field(..., gt =0,  description = "Height of the patient in cm ( example - 172 cm")]
    weight : Annotated[float, Field(..., gt =0,  description = "Weigth of the patient in kg ( example - 58 kg)")]
    diagnosis : Annotated[str, Field(..., description = " of the patient ( example - 001)")]
    status: Annotated[Literal['ongoing', 'over'], Field(..., description="Treatment status")]
    mobile: Annotated[str, Field(..., min_length=10, max_length=10, description="10 digit mobile number")]

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



@app.post("/patients")
def add_patient(patient: Patient):
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
            patient.diagnosis,
            patient.status,
            patient.mobile
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
        mobile=row[9]
    )


@app.get("/patients")
def get_all_patients():
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()

    return [
        Patient(
            id=r[0], name=r[1], age=r[2], gender=r[3],
            city=r[4], height=r[5], weight=r[6],
            diagnosis=r[7], status=r[8], mobile=r[9]
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


