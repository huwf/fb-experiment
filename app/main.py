from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    return "<html><head><title>FB Experiment</title></head><body><h1>I'm Ron Burgundy?</h1></body></html>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
