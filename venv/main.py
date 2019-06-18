from flask import Flask, url_for
from flask import render_template
from flask import flash
from flask import redirect
from flask_bootstrap import Bootstrap
from forms import RegistrationForm, LoginForm


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['SECRET_KEY'] = '419PAUL419'


@app.route('/')
@app.route('/<name>')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account creted for {form.username.data}!', 'success')
        return redirect(url_for('index'))

    return render_template("signup.html", title="Register", form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)



if __name__ == "__main__":
    app.run()