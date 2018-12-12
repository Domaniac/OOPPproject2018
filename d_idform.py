from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, Length


user_review_id = 0

class IDForm(Form):
    # preferred_name
    user_review_id = StringField('Enter review ID', validators=[DataRequired("Enter id")])
    # ('Review tags:', choices=[('faculty', 'Faculty'), ('facilities', 'Facilities'),
    # ('food', 'Food'),
    # ('Co-curricular Activities', 'Co-curricular Activities'),
    # ('Courses and subjects offered',
    # 'Courses and subjects offered')],
    # validators=[DataRequired("Enter Review body")])
    #  for app.py to flash current user id
    submit = SubmitField('Submit Review ID')

