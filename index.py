from flask import Flask, render_template,request,url_for
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
#SQ: settings
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
class user(db.Model):
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
def home():
    users=user.query.email()
    if request.method=='GET':
        #change to template for  putting in email
        return render_template('Forgot_Password.html')
    #Gets email entered in above form
    email=request.form['email']
    #Adds token
    check=1
    for user in users:
        if email==user:
            check=0
    if check==0:
      token=timer.dumps(email,salt='email-confirm')
      #Creates and sends message
      msg=Message('Confirm Email',sender='damienchew2001@gmail.com',recipients=[email])
      link=url_for('confirm_email',token=token,external=True)
      msg.body="your link is {}".format(link)
      mail.send(msg)
      #Should send an alert for feedback
      return 'The email you entered is {}.The token is {}'.format(email,token)
    else:
        return "Email does not belong to any account"

@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
      email=timer.loads(token,salt='email-confirm',max_age=100)
    except SignatureExpired:
        return "<h1>The token is expired</h1>"
    return "the token works"

@app.route("/search")
def search():
    return render_template("Search.html",teachers=teachers.query.name(),schools=schools.query.name())

@app.route("/search/Advanced_Search")
def advanced_search():
    return render_template("Advanced_Search.html",teachers=teachers.query.all(),schools=schools.query.all())

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
