from langchain.prompts import PromptTemplate

SCHEMA = """
Tables and columns in SQLite database `patients_db`:

1. patients(
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
"""

FEW_SHOTS = """
User: How many patients are there?
Answer:
1. Total number of patients is -
2. SELECT COUNT(*) AS Count FROM patients;

User: Show all patients from Delhi
Answer:
1. Patients from Delhi are -
2. SELECT id AS ID, name AS Name, age AS Age, diagnosis AS Diagnosis
   FROM patients
   WHERE city = 'Delhi';

User: Show patients whose treatment is ongoing
Answer:
1. Patients with ongoing treatment are -
2. SELECT id AS ID, name AS Name, diagnosis AS Diagnosis, status AS Status
   FROM patients
   WHERE status = 'ongoing';

User: How many male and female patients are there?
Answer:
1. Gender distribution of patients is -
2. SELECT gender AS Gender, COUNT(*) AS Count
   FROM patients
   GROUP BY gender;

User: Show patients suffering from fever
Answer:
1. Patients diagnosed with fever are -
2. SELECT id AS ID, name AS Name, age AS Age, city AS City
   FROM patients
   WHERE diagnosis LIKE '%Fever%';

User: List patients who have headache as a symptom
Answer:
1. Patients with headache symptoms are -
2. SELECT id AS ID, name AS Name, symptoms AS Symptoms
   FROM patients
   WHERE symptoms LIKE '%headache%';

User: Show average age of patients
Answer:
1. Average age of patients is -
2. SELECT AVG(age) AS AverageAge FROM patients;

User: Show patients older than 50
Answer:
1. Patients older than 50 are -
2. SELECT id AS ID, name AS Name, age AS Age
   FROM patients
   WHERE age > 50;
"""


prompt = PromptTemplate(
    input_variables=["question"],
    template=f"""
You are a healthcare database assistant.

You are an expert in SQLite queries.
Convert the user's natural language question into two parts:

1. A short natural language response template.
   - Example: "Total number of patients is -"
   - Do NOT include actual numbers unless SQL result is available.
   - Write response in user's language only.

2. A valid SQLite query.
   - Use only the given table and columns.
   - Always use column aliases with meaningful names (ID, Name, Age, City, Diagnosis, Count, etc).
   - Always return only ONE SQL query.
   - Do NOT use markdown.
   - Do NOT include ```sql.
   - Do NOT hallucinate tables or columns.
   - For chart queries, use GROUP BY with aggregation.

Schema:
{SCHEMA}

Examples:
{FEW_SHOTS}

Now generate answer for:

User: {{question}}
Answer:
"""
)