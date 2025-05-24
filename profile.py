from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.models import db, User
from forms.forms import ProfileEditForm
import os
from werkzeug.utils import secure_filename
from config import Config

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

# Profile main page view
@profile_bp.route('/')
@login_required
def profile_home():
    return render_template('profile/profile.html', user=current_user)

# Profile edit view, supports GET and POST
@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm(obj=current_user)

    if form.validate_on_submit():
        # Update username and email from form data
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Handle profile photo upload if provided
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo:
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                current_user.photo = filename  # Save filename in user model

        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('profile.profile_home'))

    return render_template('profile/edit_profile.html', form=form)
