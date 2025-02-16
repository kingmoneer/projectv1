import logging
from app.models.product import Product
from app import db

logger = logging.getLogger(__name__)


def get_all_products():
    logger.info("Fetching all products")
    return Product.query.all()


def get_product_by_id(product_id):
    logger.info(f"Fetching product with ID: {product_id}")
    return Product.query.get_or_404(product_id)


def create_product(name, description, price):
    """Create a new product"""
    logger.info(f"Creating new product: {name}")
    product = Product(name=name, description=description, price=price)
    db.session.add(product)
    db.session.commit()
    logger.info(f"Product created successfully: ID {product.id}")
    return product


def update_product(product_id, name, description, price):
    """Update an existing product"""
    logger.info(f"Updating product ID {product_id}")
    product = get_product_by_id(product_id)
    product.name = name
    product.description = description
    product.price = price
    db.session.commit()
    logger.info(f"Product ID {product_id} updated successfully")
    return product


def delete_product(product_id):
    """Delete a product"""
    logger.info(f"Deleting product ID {product_id}")
    product = get_product_by_id(product_id)
    db.session.delete(product)
    db.session.commit()
    logger.info(f"Product ID {product_id} deleted successfully")
