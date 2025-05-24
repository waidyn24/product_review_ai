from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from models.models import db, Product
from forms.forms import ProductForm, EditProductForm

products_bp = Blueprint('products', __name__, url_prefix='/products')


def allowed_file(filename):
    # Check if the file has an allowed extension
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# Product list with optional search functionality
@products_bp.route('/')
def product_list():
    search = request.args.get('q')
    if search:
        products = Product.query.filter(Product.name.ilike(f'%{search}%')).all()
    else:
        products = Product.query.all()
    return render_template('product_list.html', products=products, search=search)


# Add a new product (only accessible by admin users)
@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    # Usually only admins can add products; role check here
    if current_user.role != 'admin':
        abort(403)
    form = ProductForm()
    if form.validate_on_submit():
        filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            image_path=filename
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product successfully added.', 'success')
        return redirect(url_for('products.product_list'))

    return render_template('add_product.html', form=form)


# View product details
@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


# Edit an existing product (admin only)
@products_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.role != 'admin':
        abort(403)
    product = Product.query.get_or_404(product_id)
    form = EditProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data

        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                product.image_path = filename

        db.session.commit()
        flash('Product successfully updated.', 'success')
        return redirect(url_for('products.product_detail', product_id=product.id))

    return render_template('edit_product.html', form=form, product=product)


# Delete a product (admin only)
@products_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if current_user.role != 'admin':
        abort(403)
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'warning')
    return redirect(url_for('products.product_list'))
