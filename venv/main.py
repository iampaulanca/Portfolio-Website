from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name=None):
    return render_template("profile.html", name=name)

if __name__ == "__main__":
    app.run()