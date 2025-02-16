import logging
from flask import render_template, request, redirect, url_for, flash

logger = logging.getLogger(__name__)

from app.controllers.product_controller import (
    get_all_products, 
    get_product_by_id, 
    create_product,
    update_product,
    delete_product
)
from app.controllers.cart_controller import add_to_cart, get_cart_items, get_cart_total
from app.controllers.order_controller import create_order
from app.controllers.auth_controller import (
    register_user,
    login_user,
    logout_user,
    get_current_user
)
from app import app


from app.models.order import Order


@app.route('/')
def index():
    logger.info(f"Request received: {request.method} {request.url}")
    products = get_all_products()
    current_user = get_current_user()
    logger.info(f"Rendering index page with {len(products)} products")
    return render_template('index.html', products=products, current_user=current_user)



@app.route('/manage_products')
def manage_products():
    products = get_all_products()
    return render_template('manage_products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    logger.info(f"Request received: {request.method} {request.url}")
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        logger.info(f"Creating new product: {name}")
        create_product(name, description, price)
        flash('Product added successfully!')
        logger.info(f"Product created successfully, redirecting to manage_products")
        return redirect(url_for('manage_products'))
    logger.info("Rendering add_product form")
    return render_template('add_product.html')


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = get_product_by_id(product_id)
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        update_product(product_id, name, description, price)
        flash('Product updated successfully!')
        return redirect(url_for('manage_products'))
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    delete_product(product_id)
    flash('Product deleted successfully!')
    return redirect(url_for('manage_products'))



@app.route('/product/<int:product_id>')
def product(product_id):
    product = get_product_by_id(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart_route(product_id):
    add_to_cart(product_id)
    flash('Product added to cart!')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    logger.info(f"Request received: {request.method} {request.url}")
    cart_items = get_cart_items()
    total = get_cart_total()
    logger.info(f"Rendering cart page with {len(cart_items)} items, total: {total}")
    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        order = create_order()
        return redirect(url_for('order_confirmation', order_id=order.id))
    return render_template('checkout.html')

@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))
