from flask import Flask, render_template,request,url_for,flash
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
#SQL settings
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config['SECRET_KEY']='random string'
db = SQLAlchemy(app)
db.TRACK_MODIFICATIONS=False
#Email configs
app.config.from_pyfile('emailConfig.cfg')
mail=Mail(app)
timer=URLSafeTimedSerializer("2")
#SQL Data tables
class schools(db.Model):
    id = db.Column('shools_id', db.Integer, primary_key = True)
    category=db.Column(db.String(100))
    name=db.Column(db.String(100))
    zone=db.Column(db.String(50))
    addr=db.Column(db.String(200))
    PSLE=db.Column(db.Integer)
    L1R5=db.Column(db.Integer)
    L1R4=db.Column(db.Integer)
    def __init__(self,category,name,zone,addr):
        self.name=name
        self.zone=zone
        self.addr=addr
        self.category=category
    def set_PSLE(self,psle):
        self.PSLE=psle
    def set_L1R5(self,l1r5):
        self.L1R5=l1r5
    def set_L1R4(self,l1r4):
        self.L1R4=l1r4
class users(db.Model):
    id = db.Column('Uses_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    true = db.Column(db.String(100))
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.true = False
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_email(self):
        return self.email
    def set_email(self, email):
        self.email = email
    def set_password(self, password):
        self.password = password
    def get_true(self):
        return self.true
    def validate_true(self):
        self.true = True
class teachers(db.Model):
    id=db.Column('teachers_id',db.Integer,primary_key=True)
    category=db.Column(db.String(100))
    name=db.Column(db.String(100))
    faculty=db.Column(db.String(300))
    school=db.Column(db.String(100))
    def __init__(self,category,name,faculty,school):
        self.name=name
        self.faculty=faculty
        self.category=category
        self.school=school
#Initating SQL
db.create_all()
@app.route("/",methods={'GET',"POST"})
def Forgot_Password():
    message=None
    if request.method=='POST':
        ##user=db.session.query(users.email).all()
        user=['182290Q@mymail.nyp.edu.sg']
        email=request.form['email']
        check=1
        for u in user:
            if u==email:
                check=0
        if check==0:
            token = timer.dumps(email, salt='email-confirm')
            msg = Message('Password reset', sender='damienchew2001@gmail.com', recipients=[email])
            link = url_for('Change_Password', token=token, external=True)
            msg.body = "your link is 127.0.0.1:5000{}".format(link)
            mail.send(msg)
            # Should send an alert for feedback
            message='The email you entered is {}.The token is {}'.format(email, token)
        else:
            message="Email does not match with any known user."
    # change to template for  putting in email
    return render_template('Forgot_Password.html',message=message)

@app.route("/Forgot_Password/confirm_email/<token>")
def Change_Password(token):
    check=0
    try:
      email=timer.loads(token,salt='email-confirm',max_age=100)
    except SignatureExpired:
        check=1
    return render_template("Change_Password.html",expired=check)

@app.route("/search")
def search():
    return render_template("Search.html",teachers=db.session.query.with_entities(teachers.name).all(),schools=db.session.query.with_entities(schools.name).all())

@app.route("/search/Advanced_Search")
def advanced_search():
    return render_template("Advanced_Search.html",teachers=db.session.query(teachers).all(),schools=db.session.query(schools).all())

@app.route("/Add",methods=["GET","POST"])
def add():
    #Getting form data
    if request.method == 'POST':
        if request.form['Category']=="Schools":
            school=schools("Schools",
                           request.form['name'],
                           request.form['zone'],
                           request.form['addr'])
            if request.form['AdType']=='Secondary':
                school.set_PSLE(request.form['Adscores'])
            elif request.form['AdType']=='Poly':
                school.set_L1R4(request.form['Adscores'])
            elif request.form['AdType']=='JC':
                school.set_L1R5(request.form['Adscores'])
            db.session.add(school)
            db.session.commit()
        elif request.form['Category']=='Teachers':
            teacher=teachers(
             'Teachers',
             request.form['name'],
             request.form['faculty'],
            request.form['school'])
            db.session.add(teacher)
            db.session.commit()
    return render_template("new.html")

if __name__=="__main__":
  app.run(debug=True)
