from flask import Flask, render_template, request
from validator import validate_account
from .sql import *
app = Flask(__name__)


@app.route("/")
def index():
    return "<html><head><title>FB Experiment</title></head><body><h1>I'm Ron Burgundy?</h1></body></html>"

@app.route("/ping/<hash>")
def ping():
    pass

@app.route("/submitted", method="POST")
def submitted():
    data = request.data


@app.route("/participant_information")
def participant_information():
    return render_template('participant_information.html')

@app.route("/fb-app")
def facebook():
    render_template('fb-test.html')

#@app.route("/validate")
#def validate():
#	return validate_account(email, password)


@app.route("/debrief")
def debrief():
    return render_template('debrief.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
