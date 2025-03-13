from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

# DB config from environment variables
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB   = os.environ.get("POSTGRES_DB", "mydb")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "myuser")
POSTGRES_PASS = os.environ.get("POSTGRES_PASSWORD", "mypassword")

def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASS
    )

def init_db():
    """Create table if not exists."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return "Flask backend is running!"

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return "Missing username or password", 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return "Signup successful!"
    except Exception as e:
        return f"DB Error: {e}", 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return "Missing username or password", 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            stored_password = row[0]
            if stored_password == password:
                return f"Login successful! Welcome, {username}."
            else:
                return "Invalid password!"
        else:
            return "User not found!"
    except Exception as e:
        return f"Database error: {e}", 500

if __name__ == '__main__':
    init_db()  # Create table on startup
    app.run(host='0.0.0.0', port=5000)
