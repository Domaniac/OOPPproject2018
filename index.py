from flask import Flask, render_template,request,url_for,redirect
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,HiddenField
from wtforms.validators import InputRequired,Email
from flask_uploads import UploadSet,IMAGES,configure_uploads,AllExcept
app=Flask(__name__)

#SQL settings
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config['SQLALCHEMY_BINDS']={'teachers':'sqlite:///teachers.sqlite3',
                                'schools':'sqlite:///schools.sqlite3'}
app.config['SECRET_KEY']='random string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#File uploading
photos=UploadSet('photos',IMAGES,AllExcept(('exe','iso')))

app.config['UPLOADED_PHOTOS_DEST']='static/images/profile'
configure_uploads(app,photos)

#Email configs
app.config.from_pyfile('emailConfig.cfg')
mail=Mail(app)
timer=URLSafeTimedSerializer("2")
#WTForms
class emailForm(FlaskForm):
    email=StringField('Enter Email',validators=[InputRequired("NO Input"),Email("Invalid email")])
class passwordForm(FlaskForm):
    password=PasswordField('Enter new Password',validators=[InputRequired("Password cannot be empty")])
class AdvancedSearchForm(FlaskForm):
    category=HiddenField(validators=[InputRequired("NO CATEGORY")],id="category")
    table=HiddenField(validators=[InputRequired("NO TABLE")],id="table")
    input=HiddenField(validators=[InputRequired("NO INPUT")],id="input")
    by=HiddenField(id="by")
class QuickSearch(FlaskForm):
    name=HiddenField(validators=[InputRequired("No Search")],id="input")
#SQL Data tables
class schools(db.Model):
    __bind_key__='schools'
    id = db.Column('schools_id', db.Integer, primary_key = True)
    name=db.Column(db.String(100))
    zone=db.Column(db.String(50))
    address=db.Column(db.String(200))
    PSLE=db.Column(db.Integer)
    L1R5=db.Column(db.Integer)
    L1R4=db.Column(db.Integer)
    image=db.Column(db.String(500))
    bio=db.Column(db.String(400))
    achievement=db.Column(db.String(400))
    cohort=db.Column(db.Integer)
    type=db.Column(db.String(40))
    def __repr__(self):
        return 'school:{}'.format(self.name)

class users(db.Model):
    id = db.Column('Users_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    true = db.Column(db.String(100))
    def __repr__(self):
        return 'user:{}'.format(self.name)

class teachers(db.Model):
    __bind_key__="teachers"
    id=db.Column('teachers_id',db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    faculty=db.Column(db.String(300))
    school=db.Column(db.String(100))
    image=db.Column(db.String(500))
    bio=db.Column(db.String(400))
    achievement=db.Column(db.String(400))
    def __repr__(self):
        return 'teacher:{}'.format(self.name)

#Initating SQL tables
db.create_all()

@app.route("/Forgot_Password",methods={'GET',"POST"})
def Forgot_Password():
    message=None
    form=emailForm()
    if form.validate_on_submit():
        email=request.form['email']
        user = db.session.query(users).filter_by(email=email).first()
        if user!=None:
            token = timer.dumps(email, salt='email-confirm')
            msg = Message('Password reset', sender='damienchew2001@gmail.com', recipients=[form.email.data])
            link = url_for('Change_Password', token=token, external=True)
            msg.body = "your link is 127.0.0.1:5000{}".format(link)
            mail.send(msg)
            # Should send an alert for feedback
            user.true=token
            db.session.commit()
            message='The email you entered is {}.'.format(email)
        else:
            message="Email does not match with any known user."
    # change to template for  putting in email
    return render_template('Forgot_Password.html',message=message,form=form)

@app.route("/Forgot_Password/confirm_email/<token>",methods={'GET',"POST"})
def Change_Password(token):
    message=None
    check=0
    form1=passwordForm(prefix="form1")
    form2=emailForm(prefix="form2")
    try:
      email=timer.loads(token,salt='email-confirm',max_age=100)
    except SignatureExpired:
        check=1
        db.session.commit()
    if request.method=='POST':
           if request.form['form']=='password':
              if form1.validate_on_submit():
                 user=db.session.query(users).filter_by(true=token).first()
                 user.true=""
                 user.password=form1.password.data
                 message="Password has been changed to "+user.password
                 db.session.commit()
                 return redirect(url_for('Forgot_Password'))
           elif request.form['form']=='email':
               if form2.validate_on_submit():
                  email = form2.email.data
                  user = db.session.query(users).filter_by(email=email).first()
                  if user != None:
                     token = timer.dumps(email, salt='email-confirm')
                     msg = Message('Password reset', sender='damienchew2001@gmail.com', recipients=[form2.email.data])
                     link = url_for('Change_Password', token=token, external=True)
                     msg.body = "your link is 127.0.0.1:5000{}".format(link)
                     mail.send(msg)
                     # Should send an alert for feedback
                     user.true = token
                     db.session.commit()
                     message = 'The email you entered is {}.'.format(email)
                  else:
                     message = "Email does not match with any known user"
    return render_template("Change_Password.html",expired=int(check),message=message,form1=form1,form2=form2)

@app.route("/search",methods={'GET','POST'})
def search():
    search=None
    form=QuickSearch()
    advanced_search_link=url_for('advanced_search')
    if request.method=="POST":
        if form.validate_on_submit():
            input=form.name.data
            database=db.session.query(schools.name).all()
            sortlist={}
            for k in database:
                    for u in k:
                        count = u.count(input)
                        if not count == 0:
                            sortlist[u] = count
            search = []
            for w in sorted(sortlist, key=sortlist.get, reverse=True):
                search.append(w)
    return render_template("Search.html",form=form,advanced_search=advanced_search_link,schools=search)

@app.route("/search/Advanced_Search",methods={'GET',"POST"})
def advanced_search():
    message=None
    table=None
    displaylist=None
    form=AdvancedSearchForm()
    if request.method=="POST":
        if form.validate_on_submit():
            category=form.category.data
            table=form.table.data
            input=form.input.data
            if table=="schools":
                if category=="name":
                    database=db.session.query(schools.name).all()
                elif category == "zone":
                    database=db.session.query(schools.zone).all()
                elif category == "address":
                    database=db.session.query(schools.address).all()
                elif category == "L1R4" or category=="L1R5" or category=="PSLE":
                    check=0
                    by=form.by.data
                    if by=="range":
                         range=input.split("-")
                         if len(range)!=2:
                             message="invalid range"
                             check=1
                         elif range[0].isdigit()==False or range[1].isdigit==False:
                             message="Range is not a number"
                             check=1
                    elif by=="min":
                        if input.isdigit()==False:
                            message="min is not a number"
                            check=1
                    if check==0:
                        if by=="range":
                            range=input.split("-")
                            range.sort()
                            _min =range[0]
                            _max =range[1]
                            if category=="L1R4":
                                database=db.session.query(schools).filter(schools.L1R4>=_min,schools.L1R4<=_max).order_by(schools.L1R4.asc()).all()
                            elif category == "L1R5":
                                database=db.session.query(schools).filter(schools.L1R5>=_min,schools.L1R4<=_max).order_by(schools.L1R5.asc()).all()
                            elif category=="PSLE":
                                database=db.session.query(schools).filter(schools.PSLE>=_min,schools.PSLE<=_max).order_by(schools.PSLE.desc()).all()
                        elif by=="min":
                            _min=input
                            if category=="L1R4":
                                database=db.session.query(schools).filter(schools.L1R4>=_min).order_by(schools.L1R4.asc()).all()
                            elif category == "L1R5":
                                database=db.session.query(schools).filter(schools.L1R5>=_min).order_by(schools.L1R5.asc()).all()
                            elif category=="PSLE":
                                database=db.session.query(schools).filter(schools.PSLE>=_min).order_by(schools.PSLE.desc()).all()
                    else:
                        database=""
                else:
                    message="Invalid schools category"
                    database=""
            elif table=="teachers":
                if category=="name":
                    database=db.session.query(teachers.name).all()
                elif category=="faculty":
                    database=db.session.query(teachers.faculty).all()
                elif category=="school":
                    database=db.session.query(teachers.school).all()
                else:
                    message="Invalid teachers category"
                    database=""
            else:
                message="table value invalid"
                database=""
            if database!="":
                if database==[]:
                    message="NO results"
                else:
                    datalist=[]
                    sortlist={}
                    for k in database:
                        if category=="L1R5" or category=="L1R4" or category=="PSLE":
                            entry={}
                            entry["name"]=k.name
                            entry["zone"]=k.zone
                            entry["address"]=k.address
                            entry["link"]="http://127.0.0.1:5000/DisplaySchool/"+k.name
                            if category=="L1R5":
                                entry["adscore"]=k.L1R5
                            elif category=="L1R4":
                                entry["adscore"]=k.L1R4
                            elif category=="PSLE":
                                entry["adscore"]=k.PSLE
                            else:
                                entry["adscore"]="error"
                            datalist.append(entry)
                        else:
                            for u in k:
                                count=u.count(input)
                                if not count==0:
                                    sortlist[u]=count
                    if len(sortlist)==0:
                        table=category
                        displaylist=datalist
                    elif len(datalist)==0:
                        displaylist=[]
                        classlist=[]
                        search=[]
                        for w in sorted(sortlist,key=sortlist.get,reverse=True):
                            search.append(w)
                        for query in search:
                            if table=="schools":
                                if category=="name":
                                    object=db.session.query(schools).filter(schools.name==query)
                                    classlist.append(object)
                                elif category=="zone":
                                    object = db.session.query(schools).filter(schools.zone == query)
                                    classlist.append(object)
                                elif category == "address":
                                    object = db.session.query(schools).filter(schools.address == query)
                                    classlist.append(object)
                            elif table=="teachers":
                                if category == "name":
                                    object = db.session.query(teachers).filter(teachers.name == query)
                                    classlist.append(object)
                                elif category == "faculty":
                                    object = db.session.query(teachers).filter(teachers.faculty == query)
                                    classlist.append(object)
                                elif category == "school":
                                    object = db.session.query(teachers).filter(teachers.school == query)
                                    classlist.append(object)
                        for dog in classlist:
                            for k in dog:
                                if table=="schools":
                                    entry={}
                                    entry["name"]=k.name
                                    entry["zone"]=k.zone
                                    entry["address"]=k.address
                                    entry["link"]="http://127.0.0.1:5000/DisplaySchool/"+k.name
                                    displaylist.append(entry)
                                elif table=="teachers":
                                    entry={}
                                    entry["name"]=k.name
                                    entry["faculty"]=k.faculty
                                    entry["school"]=k.school
                                    entry["link"]="http://127.0.0.1:5000/DisplayTeacher/"+k.name
                                    displaylist.append(entry)
            if displaylist==[]:
                message="Empty table"
        else:
            message="Validation failed"
    return render_template("Advanced_Search.html",form=form,message=message,table=displaylist,category=table)

@app.route("/Add",methods=["GET","POST"])
def add():
    #Getting form data
    if request.method == 'POST':
        if request.form['Category']=="Schools":
            ##add module type for Poly and JC
            if request.form['AdType']=='Secondary':
                school = schools(
                    name=request.form['name'],
                    zone=request.form['zone'],
                    address=request.form['address'],
                    PSLE=request.form['Adscores'],
                    cohort=request.form['cohort'],
                    type='Secondary'
                )
                db.session.add(school)
            elif request.form['AdType']=='Poly':
                school = schools(
                    name=request.form['name'],
                    zone=request.form['zone'],
                    address=request.form['address'],
                    L1R4=request.form['Adscores'],
                    cohort=request.form['cohort'],
                    type='Polytechnic'
                    )
                db.session.add(school)
            elif request.form['AdType']=='JC':
                 school = schools(
                     name=request.form['name'],
                     zone=request.form['zone'],
                     address=request.form['address'],
                     L1R5=request.form['Adscores'],
                     cohort = request.form['cohort'],
                     type='Junior College'
                )
                 db.session.add(school)
            db.session.commit()
        elif request.form['Category']=='Teachers':
            teacher=teachers(
            name=request.form['name'],
            faculty=request.form['faculty'],
            school=request.form['school'],
            )
            db.session.add(teacher)
            db.session.commit()
        elif request.form['Category']=='Users':
            user=users(name=request.form['name'],
                       email=request.form['email'],
                       password=request.form['password'])
            db.session.add(user)
            db.session.commit()
    return render_template("new.html")

@app.route('/Add/moreSchool',methods=['POST','GET'])
def more():
    if request.method=="POST":
        school = db.session.query(schools).filter_by(name=request.form['name']).first()
        school.achievement=request.form['achieve']
        school.bio=request.form['bio']
        filename=photos.save(request.files['photo'],name=request.form['name']+".png")
        school.image=filename
        db.session.commit()
    return render_template("more.html")

@app.route('/Add/moreTeacher',methods=['POST','GET'])
def moreTeacher():
    if request.method=="POST":
        teacher = db.session.query(teachers).filter_by(name=request.form['name']).first()
        teacher.achievement = request.form['achieve']
        teacher.bio = request.form['bio']
        filename = photos.save(request.files['photo'], name=request.form['name'] + ".png")
        teacher.image = filename
        db.session.commit()
    return render_template("moreSchool.html")

@app.route('/DisplaySchool/<name>')
def display(name):
    school=db.session.query(schools).filter_by(name=name).first()
    if not school==None:
        name=school.name
        zone = school.zone
        address = school.address
        PSLE = school.PSLE
        L1R5 = school.L1R5
        L1R4 = school.L1R4
        bio = school.bio
        achievement = school.achievement
        cohort = school.cohort
        type = school.type
        image=school.image
        imageURL=photos.url(image)
        if PSLE==None:
            if L1R5==None:
                Adscore=L1R4
            else:
                Adscore=L1R5
        else:
            Adscore=PSLE
        return render_template('Schools.html',name=name,zone=zone,Adscore=Adscore,
                               image=imageURL,bio=bio,achievement=achievement,cohort=cohort,
                               type=type,address=address,)
    else:
        return "School not foung"

@app.route('/DisplayTeacher/<name>')
def displayTeacher(name):
    teacher=db.session.query(teachers).filter_by(name=name).first()
    if not teacher==None:
        school=teacher.school
        name=teacher.name
        faculty = teacher.faculty
        bio = teacher.bio
        achievement = teacher.achievement
        image=teacher.image
        imageURL=photos.url(image)
        return render_template('Teachers.html',name=name,school=school,
                               image=imageURL,bio=bio,achievement=achievement,faculty=faculty)
    else:
        return "Teacher not foung"

if __name__=="__main__":
  app.run(debug=True)