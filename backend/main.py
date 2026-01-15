from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.schemas import Patient, PatientUpdate
from backend import services

app = FastAPI(title="Patient Management System")

# Init DB
init_db()

# Templates + static
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------- PAGE ROUTES ----------

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

@app.get("/assistant")
def assistant_page(request: Request):
    return templates.TemplateResponse("assistant.html", {"request": request})


# ---------- API ROUTES ----------

@app.post("/patients")
def add_patient(patient: Patient):
    return services.add_patient_service(patient)

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    return services.get_patient_service(patient_id)

@app.get("/patients")
def get_all_patients():
    return services.get_all_patients_service()

@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, data: PatientUpdate):
    return services.update_patient_service(patient_id, data)

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    return services.delete_patient_service(patient_id)

@app.get("/profile/{patient_id}")
def patient_profile(request: Request, patient_id: str):
    patient = services.patient_profile_service(patient_id)
    return templates.TemplateResponse("profile.html", {"request": request, "patient": patient})

@app.post("/chat-db")
def chat_db(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question required")
    return services.chat_db_service(question)

@app.post("/predict")
def predict(payload: dict):
    symptoms = payload.get("symptoms", [])
    return services.predict_service(symptoms)
