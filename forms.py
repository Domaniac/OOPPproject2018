from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from app import User, User2, User3, User4

class RegFormTeacher(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=25)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    school = StringField('School/Institute', validators=[DataRequired(), Length(min=5, max=100)])
    awards = TextAreaField('Awards/Short Description', render_kw={"rows":70, "cols":11})
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=10, max=100, message="Not a valid input")])
    email = StringField('School Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class RegFormStudent(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
        school = StringField('School/Institute', validators=[DataRequired(), Length(min=5, max=100)])
        email = StringField('School Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Sign Up')


        def validate_username2(self, username):
            user = User2.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

        def validate_email2(self, email):
            user = User2.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')


class RegFormAlumni(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    school = StringField('School/Institute', validators=[DataRequired(), Length(min=5, max=100)])
    email = StringField('School Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username3(self, username):
        user = User3.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email3(self, email):
        user = User3.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')


class RegFormAdmin(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('School Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username4(self, username):
        user = User4.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email4(self, email):
        user = User4.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=15, max=100, message="Not a Valid Range")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')



    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')

