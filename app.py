import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, redirect, request, flash, session, logging
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required


app = Flask(__name__)

app.config['SECRET_KEY'] = '35bd600b45b32b926604c408427893c7'
# Config SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), unique=True, nullable=False)
    lastname = db.Column(db.String(25), unique=True, nullable=False)
    school = db.Column(db.String(100), unique=True, nullable=False)
    awards = db.Column(db.Text(200), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.school}', '{self.age}', '{self.email}', '{self.image_file}')"

class User2(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    school = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.school}', '{self.email}', '{self.image_file}')"

class User3(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    school = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.school}', '{self.email}', '{self.image_file}')"

class User4(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

db.create_all()

from forms import RegFormTeacher, RegFormStudent, LoginForm, UpdateAccountForm, RegFormAlumni, RegFormAdmin

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/preregister')
def preregister():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegFormStudent()
    return render_template('preregister.html', form=form)

@app.route('/registerstudent', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegFormStudent()
    if form.validate_on_submit():
        user2 = User2(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user2)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('student_register.html', title='Student Register', form=form)

@app.route('/registerteacher', methods=['GET', 'POST'])
def teacher_register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegFormTeacher()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, age=form.age.data, firstname=form.firstname.data, lastname=form.lastname.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('teacher_register.html', title='Teacher Register', form=form)

@app.route('/registeralumni', methods=['GET', 'POST'])
def alumni_register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegFormAlumni()
    if form.validate_on_submit():
        user3 = User3(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user3)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('alumni_register.html', title='Alumni Register', form=form)

@app.route('/registeradmin', methods=['GET', 'POST'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegFormAdmin()
    if form.validate_on_submit():
        user4 = User4(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user4)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('admin_register.html', title='Admin Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_pics', picture_fn)
    output_size = (120, 120)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.Age = form.Age.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

if __name__ == '__main__':
    app.run(debug=True)
