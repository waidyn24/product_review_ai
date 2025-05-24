# Product Review Platform

**Project:** Product Review Platform with AI-powered sentiment analysis of reviews.

---

## Project Description

This project is a full-featured Flask web application that allows users to register, log in, browse a catalog of products, leave reviews with ratings and sentiment analysis, and interact with reviews via likes and dislikes.

The application includes:

* User registration and login with secure password hashing
* User roles: regular user and admin
* CRUD operations for products (create, edit, delete) — admin only
* Creating, viewing, and deleting reviews
* Automatic sentiment analysis of reviews using a local ML model (TextBlob)
* Review voting system: likes and dislikes, with restrictions (no voting on own reviews, no duplicate votes)
* User profile page with editable information and profile photo upload
* User login activity visualization using Chart.js
* Light and dark theme toggle with preference saved in localStorage
* Product search by name with case-insensitive partial matching
* Secure image upload with file type validation
* Modular Flask Blueprints architecture
* SQLAlchemy ORM with SQLite backend

---

## Project Structure

* **app.py** — main Flask app setup, DB initialization, login manager, Blueprints registration
* **models/models.py** — data models (User, Product, Review, ReviewVote)
* **forms/forms.py** — WTForms for registration, login, product and review management, profile editing
* **blueprints/** — modules for auth, users, products, reviews
* **templates/** — Jinja2 HTML templates
* **static/** — static files: CSS, JS, images, uploaded files
* **migrations/** — Alembic migrations for DB schema changes

---

## Core Features and How They Work

### 1. User Registration

* Requires username, email, password, and password confirmation
* Validates input (length, email format, password matching)
* Passwords are hashed before storage
* Default role is "user"
* Redirects to login page after successful registration

### 2. Login and Authentication

* Login form with email and password
* "Remember me" option via cookies
* On successful login, login timestamp is saved for user activity tracking
* Uses Flask-Login for session management
* Protected pages require authentication

### 3. User Profile

* Displays current user info: username, email, profile photo
* Editable profile with photo upload (JPG, PNG, GIF; max 2MB)
* Old profile photo is deleted on new upload
* Login activity displayed as a bar chart using Chart.js
* Theme toggle button with saved preference
* Profile photo preview before saving

### 4. Product Catalog

* Lists all products with name, brief description, and image (if any)
* Search by product name (partial, case-insensitive)
* "Add product" button visible to admins only

### 5. Product Management (Admin Only)

* Add new products with name, description, and optional image
* Edit existing products (including image replacement)
* Delete products with confirmation
* Edit and delete buttons visible only to admins on product pages

### 6. Reviews and Ratings

* Users can leave reviews with rating (1-5) and text content
* Each review is automatically analyzed for sentiment: positive, neutral, or negative
* Reviews show rating, sentiment, author, and timestamp
* Users can like or dislike reviews (one vote per review, no voting on own reviews)
* Delete review button available only to review author and admins

### 7. Theme Switching

* Light and dark theme toggle button on every page
* Theme preference is saved to `localStorage` and applied automatically on page load
* Colors and styles adapt dynamically, including backgrounds, text, buttons, navbar, forms, cards, etc.

---

## Implementation Highlights

* Flask Blueprints enable modular project structure and easier maintenance
* SQLAlchemy ORM with Alembic for database migrations and schema management
* WTForms provide form handling and input validation
* Secure file uploads with filename sanitization (`secure_filename`) and extension checks
* Passwords stored securely using Werkzeug’s hash functions
* Interactive frontend built with Bootstrap and Chart.js
* Sentiment analysis performed locally using TextBlob (no external API calls)
* AJAX-based review voting with JSON responses and dynamic UI updates

---

## How to Run the Project

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database and apply migrations:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Start the development server:

   ```bash
   python app.py
   ```
6. Open your browser and go to `http://127.0.0.1:5000/`

---

## AI Integration

* The project includes sentiment analysis of user reviews using the TextBlob library
* Each review's text is analyzed for polarity to classify it as `positive`, `neutral`, or `negative`
* This feature provides meaningful insights into user opinions on each product

---


## Contact

* Author: Aidynbek Toleubayev
* Telegram: [@@qwerty0987_282](https://t.me/surfloo)
* Instagram: [waidyn24](https://instagram.com/waidyn24)

---

