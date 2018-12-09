from flask import Flask, render_template,request,url_for
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
#SQL config
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config['SECRET_KEY']='random string'
db = SQLAlchemy(app)
db.TRACK_MODIFICATIONS=False
#Email config
app.config.from_pyfile('emailConfig.cfg')
mail=Mail(app)
timer=URLSafeTimedSerializer("2")
#SQL tables
class schools(db.Model):
    id = db.Column('schools_id', db.Integer, primary_key = True)
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
class teachers(db.Model):
    id=db.Column('teachers_id',db.Integer,primary_key=True)
    category=db.Column(db.String(100))
    name=db.Column(db.String(100))
    faculty=db.Column(db.String(300))
    school=db.Column(db.String(300))
    def __init__(self,category,name,faculty,school):
        self.name=name
        self.faculty=faculty
        self.category=category
        self.school=school
#Creating database
db.create_all()
@app.route("/",methods={'GET',"POST"})
def home():
    if request.method=='GET':
    #replace with appropiate template
        return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
    email=request.form['email']
    #Creates token
    token=timer.dumps(email,salt='email-confirm')
    #Creates message
    msg=Message('Confirm Email',recipients=[email])
    link=url_for('confirm_email',token=token,external=True)
    msg.body="your link is {}".format(link)
    #Sends message
    mail.send(msg)
    #Sends back feedback information
    return 'The email you entered is {}.The token is {}'.format(email,token)

@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
      email=timer.loads(token,salt='email-confirm',max_age=100)
    except SignatureExpired:
    #IF token expired
        return "<h1>The token is expired</h1>"
    #IF token works
    return "the token works"

@app.route("/search")
def search():
    return render_template("Search.html",teachers=teachers.query.all(),schools=schools.query.all())

@app.route("/search/Advanced_Search")
def advanced_search():
    return render_template("Advanced_Search.html")

@app.route("/Add",methods=["GET","POST"])
def add():
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
