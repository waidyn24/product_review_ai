from app import app
from models.models import db, User

with app.app_context():
    # Find user by email
    user = User.query.filter_by(email="arman@gmail.com").first()
    if user:
        # Change role to admin
        user.role = "admin"
        db.session.commit()
        print("User has been successfully promoted to admin.")
    else:
        print("User not found.")
