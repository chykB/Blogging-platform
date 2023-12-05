from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bloghaven.models import User, Category


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(' Confirm_password',
                                   validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # Custom validation to check if the provided username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Already Exist')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Exist')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', 
                         validators=[FileAllowed(['jpg', 'png', 'svg'])])

    submit = SubmitField('Update')

    # Custom validation to check if the provided username already exists
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Already Exist')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Already Exist')
            

# Form for creating a new blog post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    post_image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'svg'])])
    category = SelectField('Category', coerce=int)

    submit = SubmitField(' CREATE POST')

    # Set category choices dynamically based on available categories in the database
    def set_category_choices(self):
        categories = Category.query.all()
        
        self.category.choices = [(category.id, category.category_name) for category in categories]


class CommentForm(FlaskForm):
    content = TextAreaField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('SUBMIT COMMENT')