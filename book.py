from db import DataBase
import sqlite3

class Book :
    def __init__(self, name, author, description, image):
        self.name = name
        self.author = author
        self.description = description
        self.image = image


    def info(self):
        return {
                'name': self.name,
                'author': self.author,
                'description':self.description}


class BookList:
    def __init__(self, db, name="My books"):
        self.db = db  # об'єкт DataBase
        self.name = name

    def add(self, user_id, title, author, description, thumbnail):
        # Викликаємо метод DataBase для додавання книги
        success, message = self.db.add_book(user_id, title, author, description, thumbnail)
        return success, message

    def all_books(self, user_id):
        # Повертаємо книги конкретного користувача
        books = self.db.check_book(user_id)
        return books
