import requests
from book import Book,BookList
from user import User
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from db import DataBase

db = DataBase('users.db')
login_manager = LoginManager()
db.creating_table('books')
book_list = BookList('users.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = '123234545677'
login_manager.init_app(app)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search():
    found_books = []
    if request.method == "POST":
        book_name = request.form.get("book")
        found_books = search_book(book_name)
    return render_template('search.html', books=found_books)

def search_book(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q={title}"
    response = requests.get(url)
    data = response.json()
    book_list = []
    for item in data.get('items', []):
        info = item.get('volumeInfo', {})
        name = info.get('title', 'N/A')
        authors = info.get('authors', ['N/A'])
        author = ', '.join(authors)
        description = info.get('description', '')
        image_links = info.get('imageLinks', {})
        thumbnail = image_links.get('thumbnail', '')
        book = Book(name, author, description,thumbnail)
        book_list.append(book)
    return book_list

@app.route('/add', methods=["POST"])
def add():
    user_id = current_user.id
    data = request.get_json()  # читаємо JSON від JS
    title = data.get("name")
    author = data.get("author")
    description = data.get("description")
    thumbnail = data.get("thumbnail")
    book = Book(title, author, description, thumbnail)
    book_list.add(user_id, title, author,description,thumbnail)
    return jsonify({"status": "success"})

@app.route('/my_list', methods = ['GET', 'POST'])
@login_required
def my_list():
    user_id = current_user.id
    books = db.check_book(user_id)
    return render_template('my_list.html',books = books)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        if not email or not name or not password:
            flash('Всі поля обов\'язкові!')
            return render_template('register.html')
        success, message = db.add_user(email, name, password)
        flash(message)
        if success:
            return redirect(url_for('search'))
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or  not password:
            flash('Всі поля обов\'язкові!')
            return render_template('login.html')
        success, message, user_data = db.check(email, password)
        flash(message)
        if success:
            user_id, password, email = user_data
            user = User(user_id, email, password)
            login_user(user)
            return redirect(url_for('search'))
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)