from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from forms.forms import ProfileEditForm
from models.models import db
import os
from werkzeug.utils import secure_filename
import json

users_bp = Blueprint('users', __name__, url_prefix='/users')

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileEditForm(obj=current_user)

    if request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Handle file upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '' and allowed_file(file.filename):
                # Remove old image if it exists
                if current_user.profile_image:
                    try:
                        os.remove(os.path.join(UPLOAD_FOLDER, current_user.profile_image))
                    except OSError:
                        pass

                # Save new image
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                current_user.profile_image = filename

        db.session.commit()
        flash('Profile successfully updated', 'success')
        return redirect(url_for('users.profile'))

    login_data = [dt.strftime('%Y-%m-%d') for dt in current_user.login_times or []]
    return render_template('profile.html', user=current_user, form=form, login_data=json.dumps(login_data))
