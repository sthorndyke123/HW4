from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbr)

app =Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE-URI']= conn
db =SQLAlchemy(app)


class Favorite_Books(db.Model):
    id = db. Column(db.Integer, primary_key=True)
    Title_of_Book = db.Column(db.String(255))
    Authors_Last_Name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | Title of Book: {1} | Author\'s Last Name:{2}".format(self.id, self.Title_of_Book,self.Authors_Last_Name)

class BookForm(FlaskForm):
    Title_of_Book = StringField('Title of Book:', validators=[DataRequired()])
    Authors_Last_Name = StringField('Author\'s Last Name:', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html', pageTitle='Favorite Books')


@app.route('/add_book', methods=['GET','POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        Book = Favorite_Books(Title_of_Book=form.Title_of_Book.data, Authors_Last_Name=form.Authors_Last_Name.data)
        db.session.add(Book)
        db.session.commit()
        return "<h2> My Favorite book is {0} {1}".format(form.Title_of_Book.data, form.Authors_Last_Name.data)

    return render_template('add_book.html', form=form, pageTitle='Add a New Book')

if __name__ == '__main__':
    app.run(debug=True)
