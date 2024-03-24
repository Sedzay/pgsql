import psycopg2

# З'єднання з базою даних
from connect import create_connection,database

# Отримати всі завдання певного користувача
def get_tasks_by_user(user_id):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
            return cur.fetchall()

# Вибрати завдання за певним статусом
def get_tasks_by_status(status_name):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s)", (status_name,))
            return cur.fetchall()

# Оновити статус конкретного завдання
def update_task_status(task_id, new_status_name):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s", (new_status_name, task_id))
            conn.commit()

# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
            return cur.fetchall()

# Додати нове завдання для конкретного користувача
def add_task_for_user(title, description, status_id, user_id):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))
            conn.commit()

# Отримати всі завдання, які ще не завершено
def get_incomplete_tasks():
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
            return cur.fetchall()

# Видалити конкретне завдання
def delete_task(task_id):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()

# Знайти користувачів з певною електронною поштою
def get_users_by_email_pattern(email_pattern):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))
            return cur.fetchall()

# Оновити ім'я користувача
def update_user_name(user_id, new_name):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))
            conn.commit()

# Отримати кількість завдань для кожного статусу
def get_task_count_by_status():
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT status.name, COUNT(tasks.id) AS task_count FROM status LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name")
            return cur.fetchall()

# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_email_domain(domain_pattern):
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT tasks.* FROM tasks INNER JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s", (domain_pattern,))
            return cur.fetchall()

# Отримати список завдань, що не мають опису
def get_tasks_without_description():
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
            return cur.fetchall()

# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_and_tasks_in_progress():
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT users.*, tasks.* FROM users INNER JOIN tasks ON users.id = tasks.user_id INNER JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress'")
            return cur.fetchall()

# Отримати користувачів та кількість їхніх завдань
def get_users_and_task_count():
    with create_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT users.id, users.fullname, COUNT(tasks.id) AS task_count FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.id, users.fullname")
            return cur.fetchall()