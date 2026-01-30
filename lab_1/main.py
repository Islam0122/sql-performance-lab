from services import SQLRunner, read_multiline_input, clean_sql, extract_table_name
from ai_model import SQLAI

if __name__ == "__main__":
    runner = SQLRunner("../database.db")
    ai = SQLAI()

    print("=" * 50)
    print("SQL AI Generator с GigaChat")
    print("=" * 50)
    print("Команды:")
    print("  - Введите описание SQL-запроса")
    print("  - 'exit' или 'quit' для выхода")
    print("  - 'tables' для просмотра таблиц")
    print("=" * 50)

    while True:
        user_command = read_multiline_input()

        if user_command.lower() in ("exit", "quit"):
            print("Выход из программы")
            break

        if user_command.lower() == "tables":
            result = runner.run_sql("SELECT name FROM sqlite_master WHERE type='table';")
            print(result)
            print("=" * 50)
            continue

        print("\n⏳ Генерация SQL...")
        sql_query = ai.generate_sql(user_command)
        sql_query_clean = clean_sql(sql_query)

        print("\n📝 Сгенерированный SQL:")
        print("-" * 50)
        print(sql_query_clean)
        print("-" * 50)

        confirmation = input("\n✅ Выполнить этот SQL? (y/n): ").strip().lower()
        if confirmation != 'y':
            print("❌ Выполнение отменено")
            print("=" * 50)
            continue

        print("\n⚙️ Выполнение SQL...")
        result = runner.run_sql(sql_query_clean)
        print("\n📊 Результат:")
        print(result)
        print("=" * 50)