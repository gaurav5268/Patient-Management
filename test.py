import sqlite3
import random

# -------- CONFIG --------
DB_PATH = "data/patients.db"
TOTAL = 200

# -------- NAMES --------
male_first = [
    "Rahul", "Amit", "Rohit", "Arjun", "Karan", "Vikas", "Suresh", "Manish", "Ankit", "Deepak",
    "Nikhil", "Akash", "Mohit", "Ravi", "Sachin", "Aman", "Pradeep", "Sunil", "Pankaj", "Harsh",
    "Rajesh", "Ajay", "Sanjay", "Vivek", "Yash", "Dev", "Shubham", "Rajat", "Varun", "Aditya"
]

female_first = [
    "Priya", "Neha", "Anjali", "Pooja", "Kavita", "Ritu", "Sneha", "Aarti", "Simran", "Nisha",
    "Kiran", "Sakshi", "Riya", "Komal", "Tanya", "Isha", "Payal", "Swati", "Meena", "Rekha",
    "Suman", "Divya", "Pallavi", "Preeti", "Shruti", "Monika", "Sheetal", "Jyoti", "Rashmi", "Kajal"
]

last_names = [
    "Sharma", "Verma", "Singh", "Gupta", "Yadav", "Patel", "Khan", "Malik", "Mehta", "Joshi",
    "Agarwal", "Chauhan", "Rajput", "Pandey", "Mishra", "Tiwari", "Jain", "Bansal", "Kapoor", "Arora",
    "Rana", "Thakur", "Saxena", "Nair", "Pillai", "Iyer", "Das", "Chatterjee", "Banerjee", "Ghosh"
]

cities = ["Delhi", "Mumbai", "Lucknow", "Varanasi", "Bangalore", "Pune", "Kolkata", "Jaipur"]
statuses = ["ongoing", "over"]

# -------- SYMPTOMS (YOUR LIST) --------
symptoms_list = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic_patches',
    'continuous_sneezing', 'shivering', 'chills', 'watering_from_eyes',
    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'vomiting', 'cough',
    'chest_pain', 'yellowish_skin', 'nausea', 'loss_of_appetite',
    'abdominal_pain', 'yellowing_of_eyes', 'burning_micturition',
    'spotting_urination', 'passage_of_gases', 'internal_itching',
    'indigestion', 'muscle_wasting', 'patches_in_throat', 'high_fever',
    'extra_marital_contacts', 'fatigue', 'weight_loss', 'restlessness',
    'lethargy', 'irregular_sugar_level', 'blurred_and_distorted_vision',
    'obesity', 'excessive_hunger', 'increased_appetite', 'polyuria',
    'sunken_eyes', 'dehydration', 'diarrhoea', 'breathlessness',
    'family_history', 'mucoid_sputum', 'headache', 'dizziness',
    'loss_of_balance', 'lack_of_concentration', 'stiff_neck',
    'depression', 'irritability', 'visual_disturbances', 'back_pain',
    'weakness_in_limbs', 'neck_pain', 'weakness_of_one_body_side',
    'altered_sensorium', 'dark_urine', 'sweating', 'muscle_pain',
    'mild_fever', 'swelled_lymph_nodes', 'malaise', 'red_spots_over_body',
    'joint_pain', 'pain_behind_the_eyes', 'constipation',
    'toxic_look_(typhos)', 'belly_pain', 'yellow_urine',
    'receiving_blood_transfusion', 'receiving_unsterile_injections',
    'coma', 'stomach_bleeding', 'acute_liver_failure',
    'swelling_of_stomach', 'distention_of_abdomen',
    'history_of_alcohol_consumption', 'fluid_overload', 'phlegm',
    'blood_in_sputum', 'throat_irritation', 'redness_of_eyes',
    'sinus_pressure', 'runny_nose', 'congestion', 'loss_of_smell',
    'fast_heart_rate', 'rusty_sputum', 'pain_during_bowel_movements',
    'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'cramps',
    'bruising', 'swollen_legs', 'swollen_blood_vessels',
    'prominent_veins_on_calf', 'weight_gain', 'cold_hands_and_feets',
    'mood_swings', 'puffy_face_and_eyes', 'enlarged_thyroid',
    'brittle_nails', 'swollen_extremeties', 'abnormal_menstruation',
    'muscle_weakness', 'anxiety', 'slurred_speech', 'palpitations',
    'drying_and_tingling_lips', 'knee_pain', 'hip_joint_pain',
    'swelling_joints', 'painful_walking', 'movement_stiffness',
    'spinning_movements', 'unsteadiness', 'pus_filled_pimples',
    'blackheads', 'scurring', 'bladder_discomfort', 'foul_smell_of_urine',
    'continuous_feel_of_urine', 'skin_peeling', 'silver_like_dusting',
    'small_dents_in_nails', 'inflammatory_nails', 'blister',
    'red_sore_around_nose', 'yellow_crust_ooze'
]

# -------- CONNECT DB --------
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

patients = []

for i in range(1, TOTAL + 1):
    gender = random.choice(["male", "female"])

    if gender == "male":
        fname = random.choice(male_first)
    else:
        fname = random.choice(female_first)

    lname = random.choice(last_names)
    full_name = f"{fname} {lname}"

    patient = (
        f"{i:03}",
        full_name,
        random.randint(10, 80),
        gender,
        random.choice(cities),
        random.randint(145, 190),
        random.randint(40, 95),
        random.choice(statuses),
        f"9{random.randint(100000000,999999999)}",
        ", ".join(random.sample(symptoms_list, random.randint(4, 8)))
    )

    patients.append(patient)

cursor.executemany("""
INSERT OR IGNORE INTO patients 
(id, name, age, gender, city, height, weight, status, mobile, symptoms)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", patients)

conn.commit()
conn.close()

print("✅ 200 realistic dummy patients inserted successfully!")
