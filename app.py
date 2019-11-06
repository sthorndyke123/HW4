from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StingField
from wtforms.validators import DataRequired

app =Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'




@app.route('/')
def index():
    return render_template('index.html', pageTitle='Horror Films')


if __name__ == '__main__':
    app.run(debug=True)
