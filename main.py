import sqlite3

def run_sql(db_path: str, sql: str):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.executescript(sql)

        if sql.strip().lower().startswith("select"):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = "Query executed successfully"

        cursor.close()
        conn.close()
        return result

    except sqlite3.Error as e:
        return f"SQL error: {e}"


def read_multiline_sql():
    print("Enter SQL code (finish with empty line):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    sql_code = read_multiline_sql()
    result = run_sql("database.db", sql_code)
    print(result)

text = input("Введи текст: ").lower()

# Разбиваем текст на слова
words = text.split()

# Множество уникальных слов
unique_words = set(words)

print("\nУникальные слова:")
for word in unique_words:
    print(word)

print("\nКоличество уникальных слов:", len(unique_words))

# Поиск повторяющихся слов
repeated = set()
seen = set()

for word in words:
    if word in seen:
        repeated.add(word)
    else:
        seen.add(word)

print("\nПовторяющиеся слова:")
for word in repeated:
    print(word)