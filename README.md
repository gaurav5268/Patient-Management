
# Patient Management System with ML-Powered Disease Prediction

## Project Overview
This project is a **Patient Management System** that combines:
- Patient database management (CRUD operations)
- Machine Learning for disease prediction using symptoms
- FIntegration of NLP + LLM for intelligent chat-based data retrieval

The goal is to build a **realistic healthcare-style backend system** where patient records are managed efficiently and smart intelligence is added using ML and AI.

---

## Objectives
- Manage patient records (Create, Read, Update, Delete)
- Allow users to select symptoms and predict possible disease using ML
- Store patient health-related data securely in a database (SQLite)
- Enable intelligent querying using NLP in the future (e.g., chat-based retrieval)
- Design the system to be scalable for AI-powered healthcare applications

---

## Features

### Patient Database Management (CRUD)
- Add new patients  
- View patient records  
- Update patient information  
- Delete patient records  
- Data stored using SQLite database  

### ✅ Machine Learning Integration
- Trained a **Random Forest model** on structured symptom data  
- Users select symptoms (multi-select)  
- Model predicts the most likely disease  
- Manual prediction pipeline created for testing  
- Achieved high accuracy (90%+ on structured dataset)

### 🚀 Upcoming AI Features (Planned)
- NLP-based search for patient data  
  Example:
  - "Show all patients with fever"
  - "How many patients are from Delhi?"
- LLM-powered assistant for chat-based hospital queries
- Retrieval-Augmented Generation (RAG) over patient records

---

## 🛠️ Tech Stack

- **Backend:** FastAPI  
- **Database:** SQLite  
- **Machine Learning:**  
  - Pandas, NumPy  
  - Scikit-learn  
  - RandomForestClassifier  
- **Model Serialization:** Pickle  
- **Future AI Integration:**  
  - NLP pipelines  
  - LLM (RAG-based querying)

---

## 🧠 Machine Learning Workflow
1. Dataset contained `Symptom_1` to `Symptom_17` columns  
2. Converted multi-column symptoms into binary symptom matrix (feature engineering)  
3. Cleaned and normalized symptom names  
4. Encoded disease labels  
5. Trained Random Forest classifier  
6. Built manual prediction function to simulate real user symptom selection  
7. Prepared model for API integration

---

## 🧪 Example Use Case

User selects symptoms:
- headache  
- nausea  
- vomiting  

System:
- Converts input into binary vector  
- Passes it to ML model  
- Returns predicted disease  
  > Example Output: **Migraine**

---


## Why This Project is Strong
- Combines **backend + database + ML**
- Demonstrates **feature engineering**
- Shows **real-world healthcare system design**
- Designed for **future NLP + LLM integration**
- Not just a toy ML notebook, but a full system

---

## Future Enhancements
- Add authentication for doctors/admin users  
- Build frontend dashboard (HTML/CSS/React)  
- Integrate LLM for natural language queries  
- Add patient report summarization using GenAI  
- Deploy on cloud (AWS/GCP)  

---

## Author
**Gaurav Chauhan**  
Bachelor of Computer Science & IT  
Focused on Python, ML, FastAPI, Data Engineering, and AI Systems

---

## ⭐ If you like this project
Give it a star ⭐ and feel free to fork and improve it!
