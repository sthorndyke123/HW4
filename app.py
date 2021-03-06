from flask import Flask, url_for
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class sthorndyke_books(db.Model):
    id = db. Column(db.Integer, primary_key=True)
    Title_of_Book = db.Column(db.String(255))
    Authors_Last_Name = db.Column(db.String(255))

def __repr__(self):
        return "id: {0} | Title of Book: {1} | Author\'s Last Name:{2}".format(self.id, self.Title_of_Book, self.Authors_Last_Name)

class BookForm(FlaskForm):
    id = IntegerField('id:')
    Title_of_Book = StringField('Title of Book:', validators=[DataRequired()])
    Authors_Last_Name = StringField('Author\'s Last Name:', validators=[DataRequired()])

@app.route('/')
def index():
    all_books = sthorndyke_books.query.all()
    return render_template('index.html',books=all_books, pageTitle='Favorite Books')


@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        print('post method')
        form = request.form
        search_value = form['search_string']
        print(search_value)
        search = "%{}%".format(search_value)
        print(search)
        results = sthorndyke_books.query.filter(or_(sthorndyke_books.Title_of_Book.like(search),
                                                    sthorndyke_books.Authors_Last_Name.like(search))).all()
        return render_template('index.html', books=results, pageTitle='Favorite Books', legend="Search Results")
    else:
        return redirect('/')



@app.route('/add_book', methods=['GET','POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = sthorndyke_books(Title_of_Book=form.Title_of_Book.data, Authors_Last_Name=form.Authors_Last_Name.data)
        db.session.add(book)
        db.session.commit()
        return redirect('/')

    return render_template('add_book.html', form=form, pageTitle='Add a New Book')

@app.route('/book/<int:id>', methods=['GET','POST'])
def delete_book(id):
    if request.method == 'POST':
        book_1= sthorndyke_books.query.get_or_404(id)
        db.session.delete(book_1)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route('/get_book/<int:id>', methods=['GET','POST'])
def get_book(id):
        book= sthorndyke_books.query.get_or_404(id)
        return render_template('book.html', form=book, pageTitle='Book Details', legend="Book Details")

@app.route('/update_book/<int:id>/update', methods=['GET','POST'])
def update_book(id):
    book = sthorndyke_books.query.get_or_404(id)
    form = BookForm()

    if form.validate_on_submit():
        book.Title_of_Book = form.Title_of_Book.data
        book.Authors_Last_Name = form.Authors_Last_Name.data
        db.session.commit()
        return redirect(url_for('get_book', id=book.id))
    form.id.data = book.id
    form.Title_of_Book.data = book.Title_of_Book
    form.Authors_Last_Name.data = book.Authors_Last_Name
    return render_template('update_book.html', form=form, pageTitle='Update Book', legend="Update A Book")



if __name__ == '__main__':
    app.run(debug=True)
