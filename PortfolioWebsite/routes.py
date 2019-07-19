from flask import url_for, render_template, flash, redirect, request
from PortfolioWebsite import app, db, bcrypt
from PortfolioWebsite.forms import RegistrationForm, LoginForm, UpdateAccountForm
from PortfolioWebsite.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))

    loginform = LoginForm()
    register_form = RegistrationForm()

    if register_form.validate_on_submit() and register_form.submit_register.data:
        hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username=register_form.username.data, email=register_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created! You are now able to log in', 'success')
        return redirect(url_for('blog'))
    elif loginform.validate_on_submit() and loginform.submit.data:
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data, duration=timedelta(seconds=20))
            flash('You have been logged in!', 'success')
            return redirect(url_for('post'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            register_form.email.data = ""
            return redirect(url_for('signup'))
    else:
        return render_template("signup.html", title="Register", register_form=register_form, loginform=loginform)


@app.route('/blog', methods=['GET'])
def blog():
    return render_template("blog.html", loginform=login())


@app.route('/post', methods=['GET', 'POST'])
def post():
    return render_template("post.html", loginform=login())


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html", loginform=login())


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))


@app.route('/profile')
@login_required
def profile():
    image_file = url_for('static', filename='img/' + current_user.image_file )
    update_form = UpdateAccountForm()
    return render_template("profile.html", title='Profile', image_file=image_file, update_form=update_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit() and loginform.submit.data:
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            flash('You have been logged in!', 'success')
            if 'profile' in request.referrer:
                return redirect(url_for('profile'))
            return redirect(url_for('blog'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return loginform
