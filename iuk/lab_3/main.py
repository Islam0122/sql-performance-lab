import sqlite3
from contextlib import closing

DB_PATH = "../database.db"


def create_db(db_path: str = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        with closing(conn.cursor()) as cursor:
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS specialty (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS student (
                cipher TEXT PRIMARY KEY,
                fio TEXT NOT NULL,
                specialty_code TEXT NOT NULL,
                FOREIGN KEY (specialty_code)
                    REFERENCES specialty(code)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_cipher TEXT NOT NULL,
                subject TEXT NOT NULL,
                grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 5),
                FOREIGN KEY (student_cipher)
                    REFERENCES student(cipher)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            """)


if __name__ == "__main__":
    create_db()