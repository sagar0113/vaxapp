from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'vaxsecret'

# MYSQL DATABASE CONNECTION
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sagar@localhost/vaxapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(app)

# ---------------- DATABASE TABLES ----------------

class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(100), unique=True)
    password = DB.Column(DB.String(100))


class Vaccine(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    vaccine_name = DB.Column(DB.String(100))
    vaccine_date = DB.Column(DB.String(100))
    username = DB.Column(DB.String(100))

# ---------------- INDEX PAGE ----------------

@app.route('/')
def index():
    return render_template('index.html')

# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User(
            username=username,
            password=password
        )

        DB.session.add(user)
        DB.session.commit()

        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session['username'] = username
            return redirect('/home')

        else:
            return "Invalid Username or Password"

    return render_template('login.html')

# ---------------- HOME ----------------

@app.route('/home')
def home():

    if 'username' not in session:
        return redirect('/login')

    return render_template(
        'home.html',
        username=session['username']
    )

# ---------------- ADD VACCINE ----------------

@app.route('/add_vaccine', methods=['GET', 'POST'])
def add_vaccine():

    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':

        vaccine_name = request.form['vaccine_name']
        vaccine_date = request.form['vaccine_date']

        vaccine = Vaccine(
            vaccine_name=vaccine_name,
            vaccine_date=vaccine_date,
            username=session['username']
        )

        DB.session.add(vaccine)
        DB.session.commit()

        return redirect('/view_vaccine')

    return render_template('add_vaccine.html')

# ---------------- DELETE VACCINE ----------------

@app.route('/delete_vaccine/<int:id>')
def delete_vaccine(id):

    if 'username' not in session:
        return redirect('/login')

    vaccine = Vaccine.query.get(id)

    if vaccine:
        DB.session.delete(vaccine)
        DB.session.commit()

    return redirect('/view_vaccine')

# ---------------- VIEW VACCINE ----------------

@app.route('/view_vaccine')
def view_vaccine():

    if 'username' not in session:
        return redirect('/login')

    vaccines = Vaccine.query.filter_by(
        username=session['username']
    ).all()

    return render_template(
        'view_vaccine.html',
        vaccines=vaccines
    )

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# ---------------- MAIN ----------------

if __name__ == '__main__':

    with app.app_context():
        DB.create_all()

    app.run(debug=True)