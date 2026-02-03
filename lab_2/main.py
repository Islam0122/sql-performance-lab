import psycopg2
from psycopg2.errors import UniqueViolation


DB_CONFIG = {
    "dbname": "shop",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_order(conn, user_id: int):
    """
    Бизнес-логика:
    нельзя создать заказ, если есть pending
    """
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO orders (user_id, status)
                    VALUES (%s, 'pending')
                    RETURNING id;
                """, (user_id,))
                order_id = cur.fetchone()[0]
                return order_id

    except UniqueViolation:
        raise Exception("Нельзя создать заказ: есть неоплаченный заказ")


def pay_order(conn, order_id: int):
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE orders
                SET status = 'paid'
                WHERE id = %s;
            """, (order_id,))


def get_orders(conn, user_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, status, created_at
            FROM orders
            WHERE user_id = %s
            ORDER BY created_at DESC;
        """, (user_id,))
        return cur.fetchall()


if __name__ == "__main__":
    conn = get_connection()

    user_id = 1

    try:
        order_id = create_order(conn, user_id)
        print(f"Заказ создан, id = {order_id}")
    except Exception as e:
        print(e)

    print("Все заказы пользователя:")
    for order in get_orders(conn, user_id):
        print(order)

    conn.close()