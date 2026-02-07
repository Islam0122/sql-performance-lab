import sqlite3
from datetime import datetime, timedelta

DB_NAME = "tasks.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_done INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            deadline TEXT
        )
        """)
    print("DB ready")


def add_task(title, days=1):
    deadline = datetime.now() + timedelta(days=days)
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO tasks (title, created_at, deadline) VALUES (?, ?, ?)",
            (title, datetime.now().isoformat(), deadline.isoformat())
        )
    print(f"Задача добавлена: {title}")


def complete_task(task_id):
    with get_conn() as conn:
        conn.execute(
            "UPDATE tasks SET is_done = 1 WHERE id = ?",
            (task_id,)
        )
    print(f"Задача #{task_id} выполнена")


def show_tasks():
    with get_conn() as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()

    print("\n📋 Список задач:")
    for t in tasks:
        status = "✅" if t["is_done"] else "⏳"
        print(f'{t["id"]}. {status} {t["title"]} (до {t["deadline"]})')


def analytics():
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        done = conn.execute("SELECT COUNT(*) FROM tasks WHERE is_done = 1").fetchone()[0]
        overdue = conn.execute("""
            SELECT COUNT(*) FROM tasks
            WHERE is_done = 0 AND deadline < ?
        """, (datetime.now().isoformat(),)).fetchone()[0]

    print("\n📊 Аналитика:")
    print(f"Всего задач: {total}")
    print(f"Выполнено: {done}")
    print(f"Просрочено: {overdue}")


if __name__ == "__main__":
    init_db()

    add_task("Изучить async Django", 2)
    add_task("Разобраться с Kafka", 3)
    add_task("Сделать pet-проект", 5)

    complete_task(1)

    show_tasks()
    analytics()