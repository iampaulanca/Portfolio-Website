import secrets
import os
from PIL import Image
from flask import url_for, render_template, flash, redirect, request, abort
from PortfolioWebsite import app, db, bcrypt
from PortfolioWebsite.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
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
    posts = Post.query.all()
    return render_template("blog.html", posts=posts, loginform=loginform)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        login()
    post = Post.query.get_or_404(post_id)
    print(post)
    loginform = LoginForm()
    loginform.email.data = ""
    loginform.password.data = ""
    return render_template("post.html", title=post.title, post=post, loginform=loginform)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post_form = PostForm()
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.subtitle = post_form.subtitle.data
        post.content = post_form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        post_form.title.data = post.title
        post_form.subtitle.data = post.subtitle
        post_form.content.data = post.content
    return render_template("create_post.html", title="Update Post", post_form=post_form, legend='Update Post')


@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, subtitle=post_form.subtitle.data, content=post_form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog'))
    return render_template("create_post.html", post_form=post_form, legend='New Post')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        login()
    loginform = LoginForm()
    loginform.email.data = ""
    loginform.password.data = ""
    return render_template("about.html", loginform=loginform)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))


def save_picture(form_picture):
    # random hex so there are no duplicate names
    random_hex = secrets.token_hex(8)
    # os.path.splitext splits the extension from the file name IE doSomething.exe ["doSomething","exe"]
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
@app.route('/profile', defaults={'username': None})
@login_required
def profile(username):
    if username == None:
        username = current_user.username
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
        return redirect(url_for('profile', username=update_form.username.data))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email

    image_file = url_for('static', filename='img/' + profile.image_file)
    return render_template("profile.html", profile=profile, title='Profile', image_file=image_file,
                           update_form=update_form)


# figure out cleaner way of doing a login
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    r = request.referrer.split('/')
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            flash('You have been logged in!', 'success')
            if 'profile' in request.referrer:
                return redirect(url_for('profile', username=current_user.username))
            if 'new' in request.referrer:
                return redirect(url_for('new_post', username=current_user.username))
            return redirect(r[len(r) - 1])
    flash('Login Unsuccessful. Please check email and password', 'danger')
    if 'login' == request.endpoint:
        return redirect(r[len(r) - 1])
    elif request == "GET":
        loginform.email.data = ""
        loginform.password.data = ""
    return render_template(r[len(r) - 1] + '.html', loginform=loginform)


@app.route('/post/4159882366')
def first_post():
    return render_template('first_post.html')