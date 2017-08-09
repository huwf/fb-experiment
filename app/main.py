from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return "<html><head><title>FB Experiment</title></head><body><h1>I'm Ron Burgundy?</h1></body></html>"

@app.route("/ping/<hash>")
def ping():
    pass


@app.route("/participant_information")
def participant_information():
    return render_template('participant_information.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
