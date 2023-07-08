from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy  # This library allows us to access the db with more high level code
from datetime import datetime


# Creating the app instance | if the template is not found use the second argument
app = Flask(__name__, template_folder='template')

app.config['SECRET_KEY'] = 'Application98'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)  # Creating a db instance


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # First column will be the PK
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


# Handling Http Requests
@app.route('/', methods=['GET', 'POST'])  # Home directory
def index():
    print(request.method)
    if request.method == 'POST':
        first_name = request.form['fName']  # Getting the first_name value from the form
        last_name = request.form['lName']
        email = request.form['email']
        date = request.form['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d')  # Converting the string date to a object
        occupation = request.form['occupation']

        # Storing the data in a table
        form = Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        flash(f'{first_name} Your Form Was Submitted Successfully!', 'success')

    return render_template("index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=8080)  # Executing the webapp
