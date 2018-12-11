from flask import Flask, render_template, flash, request
from form import SignupForm, user_idf, user_id, user_rating, user_name, user_rtitle, user_rbody

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
    user_idf()
    if request.method == "POST":
        new_preferred_name = form.preferred_name.data
        new_review_title = form.review_title.data
        new_review_body = form.review_body.data
        new_review_rating = form.review_rating.data
        user_name.append(new_preferred_name)
        user_rtitle.append(new_review_title)
        user_rbody.append(new_review_body)
        user_rating.append(new_review_rating)
        flash("Review submitted! Your review id ( for editing it later) is: " + (
                str(form.users_id[len(form.users_id) - 1]) + str(user_rating[1])))
        return render_template("Dtemplate17112018/index.html", user_name=user_name, user_rtitle=user_rtitle,
                               user_rbody=user_rbody, user_rating=user_rating, user_id=user_id)
    elif request.method == "GET":
        return render_template('Dtemplate17112018/TestReviewForm1.html', form=form)


@app.route("/ReviewForm1")
def asd():
    form = SignupForm()
    if request.method == "POST":
        return render_template("Dtemplate17112018/index.html")
    elif request.method == "GET":
        return render_template('Dtemplate17112018/TestReviewForm1.html', form=form)


if __name__ == '__main__':
    app.run()
