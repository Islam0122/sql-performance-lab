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
balance = 10000

while True:
    print("\nВаш текущий баланс:", balance)
    print("Выберите действие:")
    print("1 - Проверить баланс")
    print("2 - Снять деньги")
    print("3 - Пополнить счёт")
    print("4 - Выход")

    choice = input("Введите номер действия: ")

    if choice == "1":
        print("Ваш баланс:", balance)

    elif choice == "2":
        amount = input("Введите сумму для снятия: ")

        if not amount.isdigit():
            print("Ошибка! Введите положительное число.")
            continue

        amount = int(amount)

        if amount <= 0:
            print("Сумма должна быть больше 0.")
        elif amount > balance:
            print("Недостаточно средств.")
        else:
            balance -= amount
            print("Вы успешно сняли", amount)
            print("Новый баланс:", balance)

    elif choice == "3":
        amount = input("Введите сумму для пополнения: ")

        if not amount.isdigit():
            print("Ошибка! Введите положительное число.")
            continue

        amount = int(amount)

        if amount <= 0:
            print("Сумма должна быть больше 0.")
        else:
            balance += amount
            print("Счёт пополнен на", amount)
            print("Новый баланс:", balance)

    elif choice == "4":
        print("Спасибо за использование банкомата!")
        break

    else:
        print("Неверный пункт меню. Попробуйте снова.")


phone_book = {}

while True:
    print("\n1 - Добавить контакт")
    print("2 - Найти контакт")
    print("3 - Удалить контакт")
    print("4 - Показать все контакты")
    print("5 - Выход")

    choice = input("Выберите действие: ")

    if choice == "1":
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        phone_book[name] = phone
        print("Контакт добавлен!")

    elif choice == "2":
        name = input("Введите имя для поиска: ")
        if name in phone_book:
            print("Номер:", phone_book[name])
        else:
            print("Контакт не найден")

    elif choice == "3":
        name = input("Введите имя для удаления: ")
        if name in phone_book:
            del phone_book[name]
            print("Контакт удалён")
        else:
            print("Контакт не найден")

    elif choice == "4":
        if phone_book:
            for name, phone in phone_book.items():
                print(f"{name} : {phone}")
        else:
            print("Телефонная книга пустая")

    elif choice == "5":
        print("Выход из программы")
        break

    else:
        print("Неверный выбор")
# main.py

# Хранилище данных
tasks_list = []   # список задач (порядок)
tasks_set = set() # уникальные задачи (быстрая проверка)


# -------- Бизнес логика --------
def add_task(task: str):
    task = task.strip().lower()

    if not task:
        print("❌ Задача не может быть пустой")
        return

    if task in tasks_set:
        print("⚠️ Такая задача уже существует")
        return

    tasks_list.append(task)
    tasks_set.add(task)
    print(f"✅ Задача '{task}' добавлена")


def remove_task(task: str):
    task = task.strip().lower()

    if task not in tasks_set:
        print("❌ Задача не найдена")
        return

    tasks_list.remove(task)
    tasks_set.remove(task)
    print(f"🗑 Задача '{task}' удалена")


def show_tasks():
    if not tasks_list:
        print("📭 Список задач пуст")
        return

    print("\n📋 Список задач:")
    for i, task in enumerate(tasks_list, start=1):
        print(f"{i}. {task}")


def unique_count():
    print(f"🔢 Уникальных задач: {len(tasks_set)}")


# -------- Главный запуск (main) --------
def main():
    while True:
        print("\n=== МЕНЮ ===")
        print("1 - Добавить задачу")
        print("2 - Удалить задачу")
        print("3 - Показать задачи")
        print("4 - Кол-во уникальных задач (set)")
        print("5 - Выход")

        choice = input("Выбери действие: ")

        if choice == "1":
            task = input("Введите задачу: ")
            add_task(task)

        elif choice == "2":
            task = input("Введите задачу для удаления: ")
            remove_task(task)

        elif choice == "3":
            show_tasks()

        elif choice == "4":
            unique_count()

        elif choice == "5":
            print("Выход из программы...")
            break

        else:
            print("❌ Неверный выбор")


# Точка входа (как в реальных проектах)
if __name__ == "__main__":
    main()