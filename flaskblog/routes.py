from flask import render_template,url_for, redirect, flash, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

blog_posts = [
    {
       'author':  'Utsav Jaiswal',
       'title': 'My first blog',
       'content': 'First post comment',
       'date_posted': 'May 7th, 2024',
    },
    {
       'author':  'Another Jaiswal',
       'title': 'My second blog',
       'content': 'Not the first post comment',
       'date_posted': 'May 8th, 2024',
    },

]


@app.route('/')
@app.route('/home')
def home():
    return render_template("homepage.html", posts = blog_posts, title = 'Flask App')

@app.route('/about')
def about():
    return render_template("about.html", title = 'About')

@app.route('/register', methods = [ 'GET', 'POST'])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,
                    password = hashed_pw,
                    email = form.email.data,
                    )
        
        db.session.add(user)
        db.session.commit()
        flash(f'Your acount has been created, login to continue!', category='success')
        return redirect(url_for('login'))
    return render_template("register.html", title = 'Register',form = form)

@app.route('/login', methods = ["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            # flash('You have been logged in admin!', 'success')
            return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
            flash('Couldnt log in', 'danger')
    return render_template("login.html", title = 'Log In',form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename =  f'profile_pics/{current_user.image_file}')
    return render_template("account.html",title = 'Account', image_file = image_file)