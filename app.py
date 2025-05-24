from flask import Flask, redirect, url_for
from models.models import db
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from models.models import User
from blueprints.auth import auth_bp
from blueprints.products import products_bp
from blueprints.reviews import reviews_bp
from blueprints.users import users_bp  # ⬅️ ADDED
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Redirect from home page to product catalog
@app.route('/')
def home():
    return redirect(url_for('products.product_list'))

# Context processor for current year
@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(users_bp)

# Create upload folder if it does not exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
