from flask import Flask, render_template, flash, request
from form import SignupForm

app = Flask(__name__)

app.secret_key = "development-key"


@app.route('/index', methods=["GET", "POST"])
def load_school():
    if request.method == "POST":
        return 'Posted review!'
    else:
        return render_template("Dtemplate17112018/index.html")


# @app.route('/ReviewForm1.html')
# def review_form():
    # return render_template("Dtemplate17112018/ReviewForm1.html")


@app.route("/ReviewForm1.html", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        flash('Review submitted')
        return render_template("Dtemplate17112018/index.html")
    elif request.method == "GET":
        return render_template('Dtemplate17112018/TestReviewForm1.html', form=form)



if __name__ == '__main__':
    app.run()
