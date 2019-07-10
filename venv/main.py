from flask import Flask, url_for
from flask import render_template
from flask import flash
from flask import redirect
from flask_bootstrap import Bootstrap
from forms import RegistrationForm, LoginForm
from waitress import serve


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()
app.config['SECRET_KEY'] = 'TEMP'


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

    loginform = LoginForm()
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('blog'))
    elif loginform.validate_on_submit():
        if loginform.email.data == 'admin@blog.com' and loginform.password.data == 'password':
            print("admin and password")
            flash('You have been logged in!', 'success')
            return redirect(url_for('blog'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template("signup.html", title="Register", form=form, loginform=loginform)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        if loginform.email.data == 'admin@blog.com' and loginform.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('blog'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("blog.html", loginform=loginform)


@app.route('/post')
def post():
    return render_template("post.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
