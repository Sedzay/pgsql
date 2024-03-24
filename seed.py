from faker import Faker
import psycopg2
import random
from connect import create_connection,database


# Створення об'єкту Faker
fake = Faker()

# Функція для заповнення таблиці users
def seed_users(conn):
    cur = conn.cursor()
    for _ in range(10):  # створимо 10 користувачів
        fullname = fake.name()
        email = fake.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    conn.commit()

# Функція для заповнення таблиці tasks
def seed_tasks(conn):
    cur = conn.cursor()
    status_ids = [1, 2, 3]  # статуси, які ми вже додали у таблицю status
    user_ids = [i for i in range(1, 11)]  # ідентифікатори користувачів
    for _ in range(20):  # створимо 20 завдань
        title = fake.sentence()
        description = fake.paragraph()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", 
                    (title, description, status_id, user_id))
    conn.commit()

# Функція для заповнення таблиці status
def seed_status(conn):
    cur = conn.cursor()
    status_names = ['new', 'in progress', 'completed']
    for name in status_names:
        cur.execute("INSERT INTO status (name) VALUES (%s)", (name,))
    conn.commit()


if __name__ == '__main__':
    with create_connection(database) as conn:

        seed_users(conn)
        seed_status(conn)
        seed_tasks(conn)
        