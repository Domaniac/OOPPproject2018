from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, Length

user_id = [0]
user_name = ["Test username"]
user_rtitle = ["Test title"]
user_rbody = ["Test review"]
user_rating = [5]
preferred_name = ""
review_title = ""
review_body = ""
review_rating = 0


class SignupForm(Form):
    preferred_name = StringField('Preferred name', validators=[DataRequired("Enter name")])
    review_title = StringField('Title of Review', validators=[DataRequired("Enter Review title")])
    review_body = TextAreaField("Review:", validators=[DataRequired("Enter Review body")])
    review_rating = SelectField('Overall Rating:', choices=[('1 Star', '1 Star'), ('2 Star', '2 Star'),
                                                            ('3 Star', '3 Star'), ('4 Star', '4 Star'),
                                                            ('5 Star', '5 Star')],
                                validators=[DataRequired("Enter Review body")], default='five stars')
    review_tags = RadioField('Post as anonymous?', choices=[('Yes', 'Yes'), ('No', 'No')], default='N')
    # ('Review tags:', choices=[('faculty', 'Faculty'), ('facilities', 'Facilities'),
    # ('food', 'Food'),
    # ('Co-curricular Activities', 'Co-curricular Activities'),
    # ('Courses and subjects offered',
    # 'Courses and subjects offered')],
    # validators=[DataRequired("Enter Review body")])
    users_id = user_id # for app.py to flash current user id
    submit = SubmitField('Submit Review')


def user_idf():
    new_user_id = user_id[len(user_id)-1] + 1
    user_id.append(new_user_id)
    print('appended user_id')
    for i in range(len(user_id)):
        print(user_id[i])
