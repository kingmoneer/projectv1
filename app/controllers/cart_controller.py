import logging
from app.models.cart import Cart
from app.models.product import Product
from app import db

logger = logging.getLogger(__name__)

def add_to_cart(product_id):
    """Add a product to the cart"""
    logger.info(f"Adding product ID {product_id} to cart")
    try:
        product = Product.query.get_or_404(product_id)
        cart_item = Cart(product_id=product_id)
        db.session.add(cart_item)
        db.session.commit()
        logger.info(f"Product ID {product_id} added to cart successfully")
    except Exception as e:
        logger.error(f"Error adding product {product_id} to cart: {str(e)}")
        raise

def get_cart_items():
    """Get all items in the cart"""
    logger.info("Fetching all cart items")
    try:
        items = Cart.query.all()
        logger.info(f"Found {len(items)} items in cart")
        return items
    except Exception as e:
        logger.error(f"Error retrieving cart items: {str(e)}")
        raise

def get_cart_total():
    """Calculate the total price of items in the cart"""
    logger.info("Calculating cart total")
    try:
        cart_items = Cart.query.all()
        total = sum(item.product.price for item in cart_items)
        logger.info(f"Cart total calculated: {total}")
        return total
    except Exception as e:
        logger.error(f"Error calculating cart total: {str(e)}")
        raise
