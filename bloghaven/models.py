from bloghaven import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User Model
    
    Represents a user in the blogging platform.

    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comment = db.relationship('Comment', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    """Post Model
        Represents a blog post in the platform.

    Methods:
        __repr__: Returns a string representation of the post.
    """

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    post_image_file = db.Column(db.String(20), nullable=False, default='default_image.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    comment = db.relationship('Comment', backref='post', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='posts')
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.description}', '{self.post_image_file}')"
    

class Category(db.Model):
    """Category Model
    
    Represents a category to which posts belong.

    Methods:
        __repr__: Returns a string representation of the category.

    """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100))

    def __repr__(self):
        return f"Category('{self.category_name}')"
    

class Comment(db.Model):
    """Comment Model
        Represents a comment on a blog post.

    Methods:
        __repr__: Returns a string representation of the comment.

    """
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}' '{self.user_id}')"