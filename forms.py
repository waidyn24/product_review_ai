from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    TextAreaField, FileField, IntegerField, BooleanField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError
from flask_wtf.file import FileAllowed

# Registration form
class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="This field is required"),
            Length(min=3, max=25, message="Length must be between 3 and 25 characters")
        ],
        render_kw={"class": "form-control", "placeholder": "Enter username"}
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="This field is required"),
            Email(message="Enter a valid email address")
        ],
        render_kw={"class": "form-control", "placeholder": "Enter email"}
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="This field is required"),
            Length(min=6, message="Password must be at least 6 characters")
        ],
        render_kw={"class": "form-control", "placeholder": "Enter password"}
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(message="This field is required"),
            EqualTo('password', message="Passwords must match")
        ],
        render_kw={"class": "form-control", "placeholder": "Confirm password"}
    )
    submit = SubmitField(
        'Register',
        render_kw={"class": "btn btn-primary"}
    )

# Login form
class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(message="This field is required"), Email()],
        render_kw={"class": "form-control", "placeholder": "Enter email"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="This field is required")],
        render_kw={"class": "form-control", "placeholder": "Enter password"}
    )
    remember = BooleanField('Remember me')
    submit = SubmitField(
        'Login',
        render_kw={"class": "btn btn-primary"}
    )

# Product addition form
class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('Image (optional)')
    submit = SubmitField('Add product')

# Product editing form
class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image = FileField('New image (optional)')
    submit = SubmitField('Save changes')

# Review form
class ReviewForm(FlaskForm):
    content = TextAreaField('Your review', validators=[DataRequired()])
    rating = IntegerField('Rating (1–5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit review')

# Profile edit form with photo validation
class ProfileEditForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="This field is required"),
            Length(min=3, max=25, message="Length must be between 3 and 25 characters")
        ],
        render_kw={"class": "form-control", "placeholder": "Enter username"}
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="This field is required"),
            Email(message="Enter a valid email address")
        ],
        render_kw={"class": "form-control", "placeholder": "Enter email"}
    )
    photo = FileField(
        'Profile photo',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only images are allowed (JPG, PNG, GIF)')
        ],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        'Save changes',
        render_kw={"class": "btn btn-primary"}
    )

    def validate_photo(self, field):
        if field.data:
            filename = field.data.filename.lower()
            if not (filename.endswith('.jpg') or
                    filename.endswith('.jpeg') or
                    filename.endswith('.png') or
                    filename.endswith('.gif')):
                raise ValidationError('Unsupported image format')
