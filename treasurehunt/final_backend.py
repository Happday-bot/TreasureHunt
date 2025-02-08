from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class LoginRequest(BaseModel):
    username: str
    password: str

class AnswerRequest(BaseModel):
    user_id: int
    answer: str

class HintRequest(BaseModel):
    user_id: int

# 1. Login Endpoint
@app.post("/login")
async def login(data: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM users WHERE username = ?", (data.username,))
    user = cursor.fetchone()

    if not user or user["password"] != data.password:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user_id = user["id"]

    cursor.execute("SELECT location_count FROM location_summary WHERE user_id = ?", (user_id,))
    location_count = cursor.fetchone()["location_count"]

    location_column = f"location{location_count}"
    cursor.execute(f"SELECT {location_column} FROM user_locations WHERE user_id = ?", (user_id,))
    location_name = cursor.fetchone()[0]

    print(location_name)


    cursor.execute("SELECT q1 FROM location_answers WHERE location_name = ?", (location_name,))
    q1 = cursor.fetchone()[0]

    conn.close()
    return {"user_id": user_id, "location_name": location_name, "q1": q1}

# 2. Submit Answer Endpoint
@app.post("/submit_answer")
async def submit_answer(data: AnswerRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT location_count FROM location_summary WHERE user_id = ?", (data.user_id,))
    location_count = cursor.fetchone()["location_count"]

    location_column = f"location{location_count}"
    cursor.execute(f"SELECT {location_column} FROM user_locations WHERE user_id = ?", (data.user_id,))
    location_name = cursor.fetchone()[0]

    cursor.execute("SELECT possible_answers FROM location_answers WHERE location_name = ?", (location_name,))
    possible_answers = cursor.fetchone()[0].split(", ")

    if data.answer in possible_answers:
        new_location_count = location_count + 1
        cursor.execute("UPDATE location_summary SET location_count = ? WHERE user_id = ?", (new_location_count, data.user_id))

        new_location_column = f"location{new_location_count}"
        cursor.execute(f"SELECT {new_location_column} FROM user_locations WHERE user_id = ?", (data.user_id,))
        new_location_name = cursor.fetchone()[0]

        cursor.execute("SELECT q1 FROM location_answers WHERE location_name = ?", (new_location_name,))
        q1 = cursor.fetchone()[0]

        conn.commit()
        conn.close()
        return {"location_name": new_location_name, "q1": q1}

    conn.close()
    raise HTTPException(status_code=400, detail="Incorrect answer")

# 3. Get Hint Endpoint
@app.post("/get_hint")
async def get_hint(data: HintRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT hint_count FROM location_summary WHERE user_id = ?", (data.user_id,))
    hint_count = cursor.fetchone()["hint_count"]

    if hint_count > 0:
        cursor.execute("SELECT location_count FROM location_summary WHERE user_id = ?", (data.user_id,))
        location_count = cursor.fetchone()["location_count"]

        location_column = f"location{location_count}"
        cursor.execute(f"SELECT {location_column} FROM user_locations WHERE user_id = ?", (data.user_id,))
        location_name = cursor.fetchone()[0]

        hint_column = f"q{hint_count + 1}"
        cursor.execute(f"SELECT {hint_column} FROM location_answers WHERE location_name = ?", (location_name,))
        hint_question = cursor.fetchone()[0]

        cursor.execute("UPDATE location_summary SET hint_count = hint_count - 1 WHERE user_id = ?", (data.user_id,))
        conn.commit()

        conn.close()
        return {"hint_question": hint_question, "remaining_hints": hint_count - 1}

    conn.close()
    raise HTTPException(status_code=400, detail="No hints left")


#4. admin views the results
@app.get("/get_result")
async def get_result():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT users.username, location_summary.* 
        FROM location_summary 
        JOIN users ON location_summary.user_id = users.id
    """)
    
    results = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7153)
