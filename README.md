
# Patient Management System

## Project Overview

The **Patient Management System** is a healthcare-style application that demonstrates how **backend systems**, **machine learning**, and **AI** can work together in a real-world scenario.

The system combines:

-   Patient record management (CRUD operations)
    
-   Machine Learning–based disease prediction
    
-   Planned AI-powered natural language querying
    

----------

## Objectives

-   Manage patient records (Create, Read, Update, Delete)
    
-   Allow users to select symptoms and predict possible diseases using ML
    
-   Store patient health-related data securely in an SQLite database
    
-   Enable intelligent querying using NLP (chat-based retrieval in the future)
    
-   Design the system to be scalable for AI-powered healthcare applications
    

----------

## Features

### Patient Database Management (CRUD)

-   Add new patients
    
-   View patient records
    
-   Update patient information
    
-   Delete patient records
    
-   Data stored using **SQLite**
    

### Machine Learning Integration

-   Trained a **Random Forest Classifier** on a structured symptom dataset
    
-   Users select symptoms using a multi-select input
    
-   Model predicts the most likely disease
    
-   Feature engineering performed by converting symptoms into binary vectors
    
-   Model saved using **Pickle** and integrated with a **FastAPI** backend
    

###  AI Features

Example queries:

-   `"Show all patients with fever"`
    
-   `"How many patients are from Delhi?"`
    
-   LLM-powered assistant for chat-based hospital queries
    
    

----------

## Tech Stack

### Backend

-   FastAPI
    

### Database

-   SQLite
    

### Machine Learning

-   Pandas
    
-   NumPy
    
-   Scikit-learn
    
-   RandomForestClassifier
    

### Model Serialization

-   Pickle
    

### AI (Planned)

-   NLP pipelines
    
-   Large Language Models (LLMs) for natural language database querying
    

----------

## Machine Learning Workflow

1.  Dataset contained multiple symptom columns (`Symptom_1` to `Symptom_17`)
    
2.  Symptoms transformed into a binary feature matrix (feature engineering)
    
3.  Cleaned and normalized symptom names
    
4.  Encoded disease labels using `LabelEncoder`
    
5.  Trained a **Random Forest Classifier**
    
6.  Created a manual prediction pipeline to simulate real user symptom selection
    
7.  Integrated the trained model with the backend API
    

----------

## Example Use Case

### User Input

Selected symptoms:

-   headache
    
-   nausea
    
-   vomiting
    

### System Workflow

1.  Symptoms are converted into a binary feature vector
    
2.  Feature vector is passed to the Random Forest model
    
3.  Model predicts the disease
    

### Example Output

```
Predicted Disease: Migraine

```

----------

## Future Enhancements

-   Secure authentication and role-based access
    
-   Advanced analytics dashboard
    
-   Full conversational AI interface for hospital staff
    
-   Deployment with Docker and cloud infrastructure
    

----------

## Disclaimer

This project is for **educational and demonstration purposes only** and is not intended for real-world medical diagnosi