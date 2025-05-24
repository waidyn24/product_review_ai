from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from models.models import db, User
from forms.forms import LoginForm, RegistrationForm
from datetime import datetime  # Import datetime for recording login times

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='user',  # Default role assigned upon registration
            login_times=[]  # Initialize login_times as an empty list at registration
        )
        user.set_password(form.password.data)  # Hash and set the user password
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)  # Log the user in, remember if checked

            # Add the current UTC time to login_times after successful login
            if user.login_times is None:
                user.login_times = []
            user.login_times.append(datetime.utcnow())
            db.session.commit()

            flash('You have successfully logged in.', 'success')
            return redirect(url_for('products.product_list'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
