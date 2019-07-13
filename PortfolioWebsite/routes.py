from flask import url_for, render_template, flash, redirect
from PortfolioWebsite import app, db, bcrypt
from PortfolioWebsite.forms import RegistrationForm, LoginForm
from PortfolioWebsite.models import User, Post
from flask_login import login_user, current_user, logout_user
from datetime import timedelta

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))

    loginform = LoginForm()
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created! You are now able to log in', 'success')
        return redirect(url_for('blog'))

    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data, duration=timedelta(seconds=20))
            flash('You have been logged in!', 'success')
            return redirect(url_for('post'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template("signup.html", title="Register", form=form, loginform=loginform)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('post'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("blog.html", loginform=loginform)


@app.route('/post', methods=['GET', 'POST'])
def post():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('post'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("post.html", loginform=loginform)


@app.route('/about', methods=['GET', 'POST'])
def about():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('post'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("about.html", loginform=loginform)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))


@app.route('/profile')
def profile():
    return render_template("profile.html")
