import sqlite3
import sys


def connect_db():
    """Подключение к базе данных"""
    try:
        conn = sqlite3.connect('../database.db')
        conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        sys.exit(1)


def show_all_specialities(conn):
    """Показать все специальности"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Специальность')

    print("\n" + "=" * 80)
    print("СПЕЦИАЛЬНОСТИ")
    print("=" * 80)
    print(f"{'Код':<12} {'Наименование'}")
    print("-" * 80)

    for row in cursor.fetchall():
        print(f"{row['КодСпециальности']:<12} {row['НаименованиеСпециальности']}")


def show_all_students(conn):
    """Показать всех студентов"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            о.Шифр,
            о.Фамилия || ' ' || о.Имя || ' ' || COALESCE(о.Отчество, '') AS ФИО,
            с.КодСпециальности,
            о.Курс,
            о.Группа,
            о.ДатаРождения,
            о.Национальность
        FROM Обучающийся о
        JOIN Специальность с ON о.КодСпециальности = с.КодСпециальности
        ORDER BY о.Курс, о.Группа, о.Фамилия
    ''')

    print("\n" + "=" * 120)
    print("СТУДЕНТЫ")
    print("=" * 120)
    print(f"{'Шифр':<8} {'ФИО':<35} {'Спец.':<12} {'Курс':<6} {'Группа':<8} {'Дата рожд.':<12} {'Нац.'}")
    print("-" * 120)

    for row in cursor.fetchall():
        print(f"{row['Шифр']:<8} {row['ФИО']:<35} {row['КодСпециальности']:<12} "
              f"{row['Курс']:<6} {row['Группа']:<8} {row['ДатаРождения']:<12} {row['Национальность']}")


def show_performance_by_student(conn, shifr):
    """Показать успеваемость конкретного студента"""
    cursor = conn.cursor()

    # Получить информацию о студенте
    cursor.execute('''
        SELECT 
            о.Фамилия || ' ' || о.Имя || ' ' || COALESCE(о.Отчество, '') AS ФИО,
            о.Курс,
            о.Группа,
            с.НаименованиеСпециальности
        FROM Обучающийся о
        JOIN Специальность с ON о.КодСпециальности = с.КодСпециальности
        WHERE о.Шифр = ?
    ''', (shifr,))

    student = cursor.fetchone()

    if not student:
        print(f"\nСтудент с шифром {shifr} не найден!")
        return

    print("\n" + "=" * 100)
    print(f"УСПЕВАЕМОСТЬ СТУДЕНТА: {student['ФИО']}")
    print(f"Специальность: {student['НаименованиеСпециальности']}")
    print(f"Курс: {student['Курс']}, Группа: {student['Группа']}")
    print("=" * 100)

    # Получить оценки
    cursor.execute('''
        SELECT 
            Семестр,
            Дисциплина,
            Оценка,
            ДатаСдачи,
            ФИОПреподавателя
        FROM Успеваемость
        WHERE Шифр = ?
        ORDER BY Семестр, ДатаСдачи
    ''', (shifr,))

    print(f"{'Сем.':<6} {'Дисциплина':<40} {'Оценка':<8} {'Дата':<12} {'Преподаватель'}")
    print("-" * 100)

    total_grade = 0
    count = 0

    for row in cursor.fetchall():
        print(f"{row['Семестр']:<6} {row['Дисциплина']:<40} {row['Оценка']:<8} "
              f"{row['ДатаСдачи']:<12} {row['ФИОПреподавателя']}")
        total_grade += row['Оценка']
        count += 1

    if count > 0:
        avg = total_grade / count
        print("-" * 100)
        print(f"Средний балл: {avg:.2f} (оценок: {count})")


def show_performance_by_subject(conn, subject):
    """Показать успеваемость по дисциплине"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            о.Фамилия || ' ' || о.Имя AS ФИО,
            о.Группа,
            у.Оценка,
            у.ДатаСдачи,
            у.ФИОПреподавателя
        FROM Успеваемость у
        JOIN Обучающийся о ON у.Шифр = о.Шифр
        WHERE у.Дисциплина = ?
        ORDER BY у.Оценка DESC, о.Фамилия
    ''', (subject,))

    results = cursor.fetchall()

    if not results:
        print(f"\nДисциплина '{subject}' не найдена!")
        return

    print("\n" + "=" * 100)
    print(f"УСПЕВАЕМОСТЬ ПО ДИСЦИПЛИНЕ: {subject}")
    print("=" * 100)
    print(f"{'ФИО':<35} {'Группа':<8} {'Оценка':<8} {'Дата':<12} {'Преподаватель'}")
    print("-" * 100)

    total = 0
    for row in results:
        print(f"{row['ФИО']:<35} {row['Группа']:<8} {row['Оценка']:<8} "
              f"{row['ДатаСдачи']:<12} {row['ФИОПреподавателя']}")
        total += row['Оценка']

    avg = total / len(results)
    print("-" * 100)
    print(f"Средний балл: {avg:.2f} (студентов: {len(results)})")


def show_menu():
    """Показать меню"""
    print("\n" + "=" * 60)
    print("МЕНЮ ПРОСМОТРА БАЗЫ ДАННЫХ")
    print("=" * 60)
    print("1. Показать все специальности")
    print("2. Показать всех студентов")
    print("3. Показать успеваемость студента (по шифру)")
    print("4. Показать успеваемость по дисциплине")
    print("5. Статистика по группам")
    print("6. Список всех дисциплин")
    print("0. Выход")
    print("=" * 60)


def show_group_statistics(conn):
    """Показать статистику по группам"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            о.Курс,
            о.Группа,
            COUNT(DISTINCT о.Шифр) AS КоличествоСтудентов,
            ROUND(AVG(у.Оценка), 2) AS СреднийБалл,
            COUNT(у.Оценка) AS КоличествоОценок
        FROM Обучающийся о
        LEFT JOIN Успеваемость у ON о.Шифр = у.Шифр
        GROUP BY о.Курс, о.Группа
        ORDER BY о.Курс, о.Группа
    ''')

    print("\n" + "=" * 80)
    print("СТАТИСТИКА ПО ГРУППАМ")
    print("=" * 80)
    print(f"{'Курс':<8} {'Группа':<10} {'Студентов':<12} {'Средний балл':<15} {'Оценок'}")
    print("-" * 80)

    for row in cursor.fetchall():
        avg = row['СреднийБалл'] if row['СреднийБалл'] else 0
        print(f"{row['Курс']:<8} {row['Группа']:<10} {row['КоличествоСтудентов']:<12} "
              f"{avg:<15} {row['КоличествоОценок']}")


def show_all_subjects(conn):
    """Показать список всех дисциплин"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT Дисциплина, COUNT(*) as Количество
        FROM Успеваемость
        GROUP BY Дисциплина
        ORDER BY Дисциплина
    ''')

    print("\n" + "=" * 80)
    print("СПИСОК ДИСЦИПЛИН")
    print("=" * 80)
    print(f"{'Дисциплина':<50} {'Количество записей'}")
    print("-" * 80)

    for row in cursor.fetchall():
        print(f"{row[0]:<50} {row[1]}")


def main():
    """Главная функция"""
    conn = connect_db()

    while True:
        show_menu()
        choice = input("\nВыберите пункт меню: ").strip()

        if choice == '1':
            show_all_specialities(conn)
        elif choice == '2':
            show_all_students(conn)
        elif choice == '3':
            shifr = input("Введите шифр студента: ").strip()
            try:
                show_performance_by_student(conn, int(shifr))
            except ValueError:
                print("Ошибка: шифр должен быть числом!")
        elif choice == '4':
            subject = input("Введите название дисциплины: ").strip()
            show_performance_by_subject(conn, subject)
        elif choice == '5':
            show_group_statistics(conn)
        elif choice == '6':
            show_all_subjects(conn)
        elif choice == '0':
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный выбор! Попробуйте снова.")

        input("\nНажмите Enter для продолжения...")

    conn.close()


if __name__ == '__main__':
    main()