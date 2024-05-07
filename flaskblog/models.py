from flaskblog import db
from datetime import datetime
from sqlalchemy.orm import mapped_column


class User(db.Model):
    id =  mapped_column(db.Integer, primary_key=True)
    username = mapped_column(db.String(20), unique = True, nullable=False)
    email = mapped_column(db.String(120), unique = True, nullable=False)
    image_file = mapped_column(db.String(20), nullable=False, default = 'default.jpeg')
    password = mapped_column(db.String(60), nullable=False)
    post = db.relationship('Post', backref = 'author', lazy=True)
    # backref means back reference
    # in the post table, the current user will be known as the author as he posts a blog
    # lazy means the data will be loaded only when necessary
    # post wouldnt be visible as a coln tho, its just a relationship 
    
    def __repr__(self):
        return f"User( '{self.username}', '{self.email}', '{self.image_file}' )"


class Post(db.Model):
    id =  mapped_column(db.Integer, primary_key=True)
    title = mapped_column(db.String(100), nullable=False)
    date_posted = mapped_column(db.DateTime, nullable=False, default = datetime.now())
    content = mapped_column(db.Text, nullable=False)
    user_id = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post ('{self.title}', '{self.date_posted}')"

