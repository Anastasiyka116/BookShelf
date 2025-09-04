import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class DataBase():
    def __init__(self, db_name = "users.db"):
        self.db= db_name

    def creating_table(self, table_name):
        # Перевірка, щоб назва таблиці була безпечна
        if not table_name.isidentifier():
            raise ValueError("Невірна назва таблиці")

        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        # Формуємо SQL як рядок, вставляючи назву таблиці
        sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            thumbnail TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        '''
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def add_user(self, email, name, password):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                return False, "Користувач з таким email вже існує"
            hashed_password = generate_password_hash(password)

            cursor.execute('''
                        INSERT INTO users (email, name, password) 
                        VALUES (?, ?, ?)
                    ''', (email, name, hashed_password))

            conn.commit()
            conn.close()
            print("Adding to DB:", email, name)
            return True, "Користувач успішно зареєстрований"
        except sqlite3.Error as e:
            return False, f"Помилка бази даних: {e}"

    def get_all_users(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, name FROM users;')
        users = cursor.fetchall()
        conn.close()
        return users

    def check(self, email, password):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()

            # Шукаємо користувача за email
            cursor.execute('SELECT id, password FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            if not user:
                return False, "Користувача з таким email не існує"
            user_id, email, stored_hash, name = user
            # Перевіряємо пароль
            if check_password_hash(stored_hash, password):
                return True, "Ви успішно залогінились", (user_id, email, name)
            else:
                return False, "Неправильний пароль", None
        except sqlite3.Error as e:
            return False, f"Помилка бази даних: {e}"
        finally:
            conn.close()


    def add_book(self, user_id, title, author, description, thumbnail):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO books (user_id, title, author, description, thumbnail) ')
            book_exist = cursor.fetchone()
            if book_exist:
                return False, "Така книжка вже додана існує"
        except sqlite3.Error as e:
            return False, f"Помилка бази даних: {e}"
        finally:
            conn.close()

    def check_book(self, user_id):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT title, author, description, thumbnail 
                FROM books 
                WHERE user_id = ?
            ''', (user_id,))
            books = cursor.fetchall()
            return books
        except sqlite3.Error as e:
            return False, f"Помилка бази даних: {e}"
        finally:
            conn.close()
