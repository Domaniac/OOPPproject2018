from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(Form):
    preferred_name = StringField('Preferred name', validators=[DataRequired("Enter name")])
    review_title = StringField('Title of Review', validators=[DataRequired("Enter Review title")])
    review_body = TextAreaField("Review:", validators=[DataRequired("Enter Review body")])
    review_rating = SelectField('Overall Rating:', choices=[('one stars', '1 Star'), ('two stars', '2 Star'),
                                                            ('three stars', '3 Star'), ('four stars', '4 Star'),
                                                            ('five stars', '5 Star')],
                                validators=[DataRequired("Enter Review body")], default='five stars')
    review_tags = RadioField('Post as anonymous?', choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    # ('Review tags:', choices=[('faculty', 'Faculty'), ('facilities', 'Facilities'),
    # ('food', 'Food'),
    # ('Co-curricular Activities', 'Co-curricular Activities'),
    # ('Courses and subjects offered',
    # 'Courses and subjects offered')],
    # validators=[DataRequired("Enter Review body")])
    submit = SubmitField('Submit Review')
