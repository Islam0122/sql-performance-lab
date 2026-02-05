import sqlite3

def create_db():
    conn = sqlite3.connect("../database.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS specialty (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        cipher TEXT PRIMARY KEY,
        fio TEXT NOT NULL,
        specialty_code TEXT NOT NULL,
        FOREIGN KEY (specialty_code)
            REFERENCES specialty(code)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_cipher TEXT NOT NULL,
        subject TEXT NOT NULL,
        grade INTEGER NOT NULL,
        FOREIGN KEY (student_cipher)
            REFERENCES student(cipher)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
