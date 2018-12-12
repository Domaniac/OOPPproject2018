from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8tpmjpya1svn11gpi1bl9qs9wi6a6nif'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Name(FlaskForm):
    name = StringField('Name of Your School', validators=[DataRequired()])
    submit = SubmitField('Add')


class School(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"School('self.name')"


db.create_all()


@app.route('/')
@app.route('/directory')
def directory():
    schools = School.query.all()
    return render_template('poly.html', schools=schools)


@app.route('/new', methods=['GET', 'POST'])
def new_directory():
    form = Name()
    if form.validate_on_submit():
        name = School(name=form.name.data)
        db.session.add(name)
        db.session.commit()
        flash(f'{form.name.data} has been added!', 'success')
        return redirect(url_for('directory'))
    return render_template('create_new.html', title='new directory', form=form)


@app.route('/<school_name>')
def directory_school_name(school_name):
    return render_template('school_website.html', school_name=school_name)


if __name__ == '__main__':
    app.run(Debug=True)