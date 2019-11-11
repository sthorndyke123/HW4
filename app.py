from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
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
    Title_of_Book = StringField('Title of Book:', validators=[DataRequired()])
    Authors_Last_Name = StringField('Author\'s Last Name:', validators=[DataRequired()])

@app.route('/')
def index():
    all_books = sthorndyke_books.query.all()
    return render_template('index.html',books=all_books, pageTitle='Favorite Books')


@app.route('/add_book', methods=['GET','POST'])
def add_book():
    form = BookForm()
    print("before validate")
    if form.validate_on_submit():
        book = sthorndyke_books(Title_of_Book=form.Title_of_Book.data, Authors_Last_Name=form.Authors_Last_Name.data)
        db.session.add(book)
        db.session.commit()
        return redirect('/')

    return render_template('add_book.html', form=form, pageTitle='Add a New Book')




if __name__ == '__main__':
    app.run(debug=True)
