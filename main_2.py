import sqlite3
from datetime import date
from typing import List, Tuple


DB_NAME = "expenses.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL CHECK(amount > 0),
            category_id INTEGER,
            description TEXT,
            expense_date DATE NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """)
        self.conn.commit()


class ExpenseService:
    def __init__(self, db: Database):
        self.db = db

    # ---------- CATEGORY ----------
    def add_category(self, name: str):
        self.db.cursor.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)",
            (name,)
        )
        self.db.conn.commit()

    # ---------- EXPENSE ----------
    def add_expense(self, amount: float, category: str, description: str = ""):
        self.add_category(category)

        self.db.cursor.execute(
            "SELECT id FROM categories WHERE name = ?",
            (category,)
        )
        category_id = self.db.cursor.fetchone()["id"]

        self.db.cursor.execute("""
            INSERT INTO expenses (amount, category_id, description, expense_date)
            VALUES (?, ?, ?, ?)
        """, (amount, category_id, description, date.today()))

        self.db.conn.commit()

    # ---------- REPORTS ----------
    def total_expenses(self) -> float:
        self.db.cursor.execute("SELECT SUM(amount) as total FROM expenses")
        return self.db.cursor.fetchone()["total"] or 0

    def expenses_by_category(self) -> List[Tuple]:
        self.db.cursor.execute("""
        SELECT c.name, SUM(e.amount) as total
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        GROUP BY c.name
        ORDER BY total DESC
        """)
        return self.db.cursor.fetchall()

    def monthly_report(self, year: int, month: int):
        self.db.cursor.execute("""
        SELECT c.name, SUM(e.amount) as total
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE strftime('%Y', e.expense_date) = ?
          AND strftime('%m', e.expense_date) = ?
        GROUP BY c.name
        """, (str(year), f"{month:02d}"))

        return self.db.cursor.fetchall()


# ----------------- DEMO -----------------
if __name__ == "__main__":
    db = Database()
    service = ExpenseService(db)

    service.add_expense(1200, "Еда", "Супермаркет")
    service.add_expense(300, "Транспорт", "Такси")
    service.add_expense(1500, "Аренда", "Квартира")
    service.add_expense(400, "Еда", "Кафе")

    print("💰 Общие расходы:", service.total_expenses())

    print("\n📊 По категориям:")
    for row in service.expenses_by_category():
        print(f"{row['name']}: {row['total']}")

    print("\n📅 Отчет за текущий месяц:")
    today = date.today()
    for row in service.monthly_report(today.year, today.month):
        print(f"{row['name']}: {row['total']}")
