import os
import sqlite3
import pandas as pd
import re
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from backend.llm_model.prompts import prompt


load_dotenv()

# -------------------- LLM SETUP --------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set in .env file")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0.0
)

chain = prompt | llm


# -------------------- DB CONNECTION --------------------

def get_connection():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "..", "data", "patients.db")
    return sqlite3.connect(db_path)



# -------------------- SQL SAFETY --------------------

def is_safe_sql(query: str) -> bool:
    forbidden = ["drop", "delete", "update", "insert", "alter", "truncate"]
    q = query.lower()
    return not any(word in q for word in forbidden)


# -------------------- NORMALIZER --------------------

def normalize_llm_output(resp):
    if not hasattr(resp, "content"):
        return str(resp)

    content = resp.content

    if isinstance(content, list):
        return "".join(
            chunk[1]
            for chunk in content
            if isinstance(chunk, tuple) and len(chunk) == 2
        )

    return content


# -------------------- PARSER --------------------

def parse_llm_response(raw_text: str):
    raw_text = raw_text.strip()

    parts = re.split(r"\b2\.\s*", raw_text, 1)

    nlp_part = parts[0].replace("1.", "").strip()
    sql_part = parts[1].strip() if len(parts) > 1 else ""

    return nlp_part, sql_part


# -------------------- SQL RUNNER --------------------

def run_sql(query: str):
    if not query:
        return pd.DataFrame()

    if not is_safe_sql(query):
        return pd.DataFrame({"Error": ["Unsafe SQL blocked"]})

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]
        return pd.DataFrame(rows, columns=cols)

    finally:
        conn.close()


# -------------------- RESPONSE FORMATTER --------------------

def format_final_response(nlp_part: str, df: pd.DataFrame):
    if df.empty:
        return {"text": f"{nlp_part} No data found.", "data": []}

    if df.shape == (1, 1):
        value = df.iloc[0, 0]
        return {"text": f"{nlp_part} {value}", "data": df.to_dict(orient="records")}

    return {
        "text": nlp_part,
        "data": df.to_dict(orient="records")
    }


# -------------------- MAIN FUNCTION (FastAPI will call this) --------------------

def ask_database(user_query: str):
    """
    This is the function your FastAPI will call.
    """

    # Run LLM
    resp = chain.invoke(user_query)

    # Normalize output
    raw_text = normalize_llm_output(resp)

    # Extract text + SQL
    nlp_part, sql_part = parse_llm_response(raw_text)

    # Run SQL
    df = run_sql(sql_part)

    # Format output
    result = format_final_response(nlp_part, df)

    return {
        "question": user_query,
        "response_text": result["text"],
        "sql": sql_part,
        "rows": result["data"]
    }