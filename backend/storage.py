
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "retention.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS learner_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_name TEXT NOT NULL,
            topic TEXT NOT NULL,
            last_revision_date TEXT NOT NULL,
            quiz_score REAL NOT NULL,
            difficulty TEXT NOT NULL,
            retention_risk TEXT NOT NULL,
            forgetting_window TEXT NOT NULL,
            revision_timing TEXT NOT NULL,
            study_advice TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS quiz_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_name TEXT,
            topic TEXT NOT NULL,
            score REAL NOT NULL,
            total_questions INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_name TEXT NOT NULL,
            topic TEXT NOT NULL,
            message TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)


def save_analysis(data, result):
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO learner_records
            (learner_name, topic, last_revision_date, quiz_score, difficulty,
             retention_risk, forgetting_window, revision_timing, study_advice, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["learner_name"], data["topic"], data["last_revision_date"],
            float(data["quiz_score"]), data["difficulty"],
            result["retention_risk"], result["forgetting_window"],
            result["revision_timing"], result["study_advice"],
            datetime.utcnow().isoformat()
        ))
        return cur.lastrowid


def save_quiz_feedback(learner_name, topic, score, total_questions):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO quiz_feedback
            (learner_name, topic, score, total_questions, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (learner_name, topic, float(score), int(total_questions),
              datetime.utcnow().isoformat()))


def save_alert(learner_name, topic, message, risk_level):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO alerts
            (learner_name, topic, message, risk_level, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (learner_name, topic, message, risk_level,
              datetime.utcnow().isoformat()))


def get_at_risk_learners(limit=50):
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("""
            SELECT * FROM learner_records
            WHERE retention_risk IN ('High', 'Medium')
            ORDER BY created_at DESC LIMIT ?
        """, (limit,)).fetchall()]


def get_summary():
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM learner_records").fetchone()[0]
        high = conn.execute("SELECT COUNT(*) FROM learner_records WHERE retention_risk='High'").fetchone()[0]
        medium = conn.execute("SELECT COUNT(*) FROM learner_records WHERE retention_risk='Medium'").fetchone()[0]
        low = conn.execute("SELECT COUNT(*) FROM learner_records WHERE retention_risk='Low'").fetchone()[0]
        avg = conn.execute("SELECT AVG(quiz_score) FROM learner_records").fetchone()[0]
    return {
        "total_analyses": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "average_quiz_score": round(avg or 0, 2),
    }
