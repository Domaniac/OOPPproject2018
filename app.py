from flask import Flask, render_template, url_for, redirect, request, flash, session

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/events')
def events():
    return render_template('events.html')


if __name__ == '__main__':
    app.run(debug=True)
