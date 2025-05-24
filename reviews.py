from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from models.models import db, Product, Review, ReviewVote
from forms.forms import ReviewForm
from ai.sentiment import analyze_sentiment

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@reviews_bp.route('/add/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()

    if form.validate_on_submit():
        sentiment = analyze_sentiment(form.content.data)
        review = Review(
            content=form.content.data,
            rating=form.rating.data,
            sentiment=sentiment,
            author=current_user,
            product=product
        )
        db.session.add(review)
        db.session.commit()
        flash('Review successfully added.', 'success')
        return redirect(url_for('products.product_detail', product_id=product.id))

    return render_template('review_form.html', form=form, product=product)


@reviews_bp.route('/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id == current_user.id or current_user.role == 'admin':
        # Delete votes associated with this review
        ReviewVote.query.filter_by(review_id=review.id).delete()
        db.session.delete(review)
        db.session.commit()
        flash('Review deleted.', 'info')
    else:
        flash('You cannot delete this review.', 'danger')
    return redirect(url_for('products.product_detail', product_id=review.product_id))


@reviews_bp.route('/like/<int:review_id>', methods=['POST'])
@login_required
def like_review(review_id):
    review = Review.query.get_or_404(review_id)

    # Prevent voting for own review
    if review.user_id == current_user.id:
        return jsonify({'error': "You cannot vote for your own review."}), 400

    vote = ReviewVote.query.filter_by(user_id=current_user.id, review_id=review_id).first()

    if vote:
        if vote.is_like:
            return jsonify({'error': "You already liked this review."}), 400
        else:
            vote.is_like = True
            review.likes = (review.likes or 0) + 1
            if review.dislikes and review.dislikes > 0:
                review.dislikes -= 1
    else:
        vote = ReviewVote(user_id=current_user.id, review_id=review_id, is_like=True)
        db.session.add(vote)
        review.likes = (review.likes or 0) + 1

    db.session.commit()
    return jsonify({'likes': review.likes, 'dislikes': review.dislikes})


@reviews_bp.route('/dislike/<int:review_id>', methods=['POST'])
@login_required
def dislike_review(review_id):
    review = Review.query.get_or_404(review_id)

    # Prevent voting for own review
    if review.user_id == current_user.id:
        return jsonify({'error': "You cannot vote for your own review."}), 400

    vote = ReviewVote.query.filter_by(user_id=current_user.id, review_id=review_id).first()

    if vote:
        if not vote.is_like:
            return jsonify({'error': "You already disliked this review."}), 400
        else:
            vote.is_like = False
            review.dislikes = (review.dislikes or 0) + 1
            if review.likes and review.likes > 0:
                review.likes -= 1
    else:
        vote = ReviewVote(user_id=current_user.id, review_id=review_id, is_like=False)
        db.session.add(vote)
        review.dislikes = (review.dislikes or 0) + 1

    db.session.commit()
    return jsonify({'likes': review.likes, 'dislikes': review.dislikes})
