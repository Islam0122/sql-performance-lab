import sqlite3
import re


class SQLRunner:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def run_sql(self, sql: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            sql_upper = sql.strip().upper()

            if sql_upper.startswith('SELECT'):
                cursor.execute(sql)
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description] if cursor.description else []
                conn.close()

                if not results:
                    return "Запрос выполнен успешно, но данных не найдено"

                output = "\nРезультаты:\n"
                output += " | ".join(columns) + "\n"
                output += "-" * 50 + "\n"
                for row in results:
                    output += " | ".join(str(val) for val in row) + "\n"
                return output
            else:
                cursor.executescript(sql)
                conn.commit()
                affected_rows = cursor.rowcount
                conn.close()
                return f"SQL выполнен успешно. Затронуто строк: {affected_rows}"

        except sqlite3.Error as e:
            return f"Ошибка SQL: {e}"


def read_multiline_input():
    print("Введите команду (пустая строка для отправки):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


def clean_sql(sql: str) -> str:
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    sql = sql.strip()
    return sql


def replace_table_name(sql: str, new_name: str) -> str:
    if not new_name:
        return sql

    sql = re.sub(
        r'CREATE TABLE (\w+)',
        f'CREATE TABLE IF NOT EXISTS {new_name}',
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r'INSERT INTO (\w+)',
        f'INSERT INTO {new_name}',
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r'UPDATE (\w+)',
        f'UPDATE {new_name}',
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r'DELETE FROM (\w+)',
        f'DELETE FROM {new_name}',
        sql,
        flags=re.IGNORECASE
    )

    sql = re.sub(
        r'FROM (\w+)',
        f'FROM {new_name}',
        sql,
        flags=re.IGNORECASE
    )

    return sql


def extract_table_name(sql: str) -> str:
    patterns = [
        r'CREATE TABLE (?:IF NOT EXISTS )?(\w+)',
        r'INSERT INTO (\w+)',
        r'UPDATE (\w+)',
        r'DELETE FROM (\w+)',
        r'FROM (\w+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, sql, re.IGNORECASE)
        if match:
            return match.group(1)

    return None