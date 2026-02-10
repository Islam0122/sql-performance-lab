import sqlite3

# Базага кошулуу
conn = sqlite3.connect("discounts.db")
cursor = conn.cursor()

# Таблица түзүү
cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price REAL,
    discount_percent INTEGER,
    discount_amount REAL,
    final_price REAL
)
""")

# Колдонуучудан сумма алуу
price = float(input("Сатып алуу суммасын киргизиңиз: "))

# Арзандатуу логикасы
if price < 1000:
    discount_percent = 0
elif price < 3000:
    discount_percent = 5
elif price < 5000:
    discount_percent = 10
else:
    discount_percent = 15

discount_amount = price * discount_percent / 100
final_price = price - discount_amount

# Маалыматты базага сактоо
cursor.execute("""
INSERT INTO purchases (price, discount_percent, discount_amount, final_price)
VALUES (?, ?, ?, ?)
""", (price, discount_percent, discount_amount, final_price))

conn.commit()
conn.close()

# Натыйжа
print(f"Арзандатуу: {discount_percent}%")
print(f"Арзандатуу суммасы: {discount_amount}")
print(f"Акыркы сумма: {final_price}")
