# apps/backend/app.py
from flask import Flask, request, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.environ.get("POSTGRES_HOST", "postgres")
DB_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
DB_NAME = os.environ.get("POSTGRES_DB", "todo")
DB_USER = os.environ.get("POSTGRES_USER", "todo_user")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "todo_pass")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN DEFAULT FALSE
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

app = Flask(__name__)

@app.before_first_request
def startup():
    init_db()

@app.route("/health")
def health():
    return jsonify({"status":"ok"}), 200

@app.route("/todos", methods=["GET"])
def list_todos():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, title, done FROM todos ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.json or {}
    title = data.get("title")
    if not title:
        return jsonify({"error":"title required"}), 400
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO todos (title) VALUES (%s) RETURNING id, title, done", (title,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(row), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json or {}
    done = bool(data.get("done", False))
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("UPDATE todos SET done=%s WHERE id=%s RETURNING id, title, done", (done, todo_id))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error":"not found"}), 404
    return jsonify(row)

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id=%s", (todo_id,))
    changed = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if changed == 0:
        return jsonify({"error":"not found"}), 404
    return jsonify({"deleted":todo_id}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
