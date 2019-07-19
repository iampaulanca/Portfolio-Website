import secrets
import os
from PIL import Image
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


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        login()
    loginform = LoginForm()
    loginform.email.data = ""
    loginform.password.data = ""
    return render_template("blog.html", loginform=loginform)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        login()
    loginform = LoginForm()
    loginform.email.data = ""
    loginform.password.data = ""
    return render_template("post.html", loginform=loginform)


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        login()
    loginform = LoginForm()
    loginform.email.data = ""
    loginform.password.data= ""
    return render_template("about.html", loginform=loginform)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))


def save_picture(form_picture):
    # random hex so there are no duplicate names
    random_hex = secrets.token_hex(8)
    # os.path.splitext spits the extension from the file name
    _f_name, f_ext = os.path.splitext(form_picture.filename)
    # add the hex to the filename to avoid duplicate file names
    picture_fn = random_hex + f_ext
    # get the path to where we want to save the picture
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    # choose a size for the image thumb and use PILLOW module to resize
    output_size = (275, 275)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    rgb_i = i.convert('RGB')
    # save the new resized picture in the picture_path
    rgb_i.save(picture_path)
    # return the path because want to update the current picture with the picture in the file path
    return picture_fn


@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    profile = db.session.query(User).filter_by(username=username).first()
    print(profile)
    update_form = UpdateAccountForm()
    if update_form.validate_on_submit():
        if update_form.picture.data:
            picture_file = save_picture(update_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        flash('Profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email

    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template("profile.html", profile=profile, title='Profile', image_file=image_file, update_form=update_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    r = request.referrer.split('/')
    print(request.referrer, r, request.endpoint)

    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            flash('You have been logged in!', 'success')
            if 'profile' in request.referrer:
                return redirect(url_for('profile', username=current_user.username))
            return redirect(r[len(r) - 1])
    flash('Login Unsuccessful. Please check email and password', 'danger')
    if 'login' == request.endpoint:
        return redirect(r[len(r) - 1])
    elif request == "GET":
        loginform.email.data = ""
        loginform.password.data = ""
    return render_template(r[len(r)-1] + '.html', loginform=loginform)

@app.route('/home/new', methods=['GET', 'POST'])
def new_post():
    # form = PostForm()
    return render_template("create_post.html")

