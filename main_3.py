import sqlite3
from datetime import datetime, timedelta

DB_NAME = "habits.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
        """)
        conn.commit()


def add_habit(name: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO habits (name, created_at) VALUES (?, ?)",
            (name, datetime.now().isoformat())
        )
        conn.commit()


def mark_done(habit_name: str):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
        habit = cursor.fetchone()
        if not habit:
            print("❌ Привычка не найдена")
            return

        cursor.execute(
            "INSERT INTO habit_logs (habit_id, date) VALUES (?, ?)",
            (habit[0], datetime.now().date().isoformat())
        )
        conn.commit()
        print(f"✅ Отмечено: {habit_name}")


def weekly_stats():
    start_date = (datetime.now() - timedelta(days=6)).date().isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT h.name, COUNT(l.id) as done_count
        FROM habits h
        LEFT JOIN habit_logs l
        ON h.id = l.habit_id AND l.date >= ?
        GROUP BY h.name
        """, (start_date,))

        print("\n📊 Статистика за 7 дней:")
        for name, count in cursor.fetchall():
            print(f"- {name}: {count}/7")


if __name__ == "__main__":
    init_db()

    # Пример использования
    add_habit("Чтение")
    add_habit("Кодинг")
    add_habit("Спорт")

    mark_done("Кодинг")
    mark_done("Чтение")

    weekly_stats()
# Словарь соответствия английской и русской раскладки
eng_to_rus = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е',
    'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
    '[': 'х', ']': 'ъ',
    'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п',
    'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж',
    "'": 'э',
    'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и',
    'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю'
}

text = input("Введите текст в английской раскладке: ")

result = ""

for char in text.lower():
    if char in eng_to_rus:
        result += eng_to_rus[char]
    else:
        result += char  # если символа нет в словаре — оставляем как есть

print("В русской раскладке это будет:", result)