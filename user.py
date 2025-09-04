from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, name):
        self.id = id            # id з таблиці users
        self.email = email
        self.name = name