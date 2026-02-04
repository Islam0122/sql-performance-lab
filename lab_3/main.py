import sqlite3

def create_database():
    # Подключение к базе данных (если файла нет, он будет создан)
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Создание таблицы Специальность
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Специальность (
        Код_специальности TEXT PRIMARY KEY,
        Наименование_специальности TEXT NOT NULL
    )
    ''')
    
    # Создание таблицы Обучающийся
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Обучающийся (
        Шифр TEXT PRIMARY KEY,
        Фамилия TEXT NOT NULL,
        Имя TEXT NOT NULL,
        Отчество TEXT,
        Код_специальности TEXT,
        Курс INTEGER,
        Группа INTEGER,
        Дата_рождения DATE,
        Национальность TEXT,
        Адрес TEXT,
        FOREIGN KEY (Код_специальности) REFERENCES Специальность(Код_специальности)
    )
    ''')
    
    # Создание таблицы Успеваемость
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Успеваемость (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Шифр TEXT,
        Семестр INTEGER,
        Дисциплина TEXT,
        Оценка INTEGER,
        Дата_сдачи DATE,
        ФИО_преподавателя TEXT,
        FOREIGN KEY (Шифр) REFERENCES Обучающийся(Шифр)
    )
    ''')
    
    # Сохранение изменений
    conn.commit()
    print("База данных успешно создана!")
    
    # Вывод списка таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("\nСозданные таблицы:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Закрытие соединения
    conn.close()

if __name__ == "__main__":
    create_database()