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


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("index.html", title="index", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))

    return render_template("signup.html", title="Register", form=form)

@app.route('/blog')
def blog():
    return render_template("blog.html")


# @app.route('/login')
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash(f'You have been logged in', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash(f'Login unsuccessful. Please check username and password', 'danger')
#     return render_template("login.html", title="Login", form=form)

if __name__ == "__main__":
    app.run()