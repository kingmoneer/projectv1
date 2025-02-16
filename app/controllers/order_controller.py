import logging
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app import db

logger = logging.getLogger(__name__)


def create_order():
    logger.info("Creating new order")
    try:
        cart_items = Cart.query.all()
        total = sum(item.product.price * item.quantity for item in cart_items)
        logger.info(f"Calculated order total: {total}")
        
        order = Order(total=total)
        db.session.add(order)
        db.session.commit()
        logger.info(f"Order created with ID: {order.id}")
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            db.session.delete(cart_item)
            logger.info(f"Added product ID {cart_item.product_id} to order")
        
        db.session.commit()
        logger.info(f"Order {order.id} completed successfully")
        return order
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        db.session.rollback()
        raise
