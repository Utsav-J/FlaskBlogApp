from flask import render_template,url_for, redirect, flash
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash('You have been logged in admin!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Couldnt log in', 'danger')
    return render_template("login.html", title = 'Log In',form = form)
