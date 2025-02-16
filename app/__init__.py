import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# تهيئة التطبيق
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=100000, backupCount=3),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info('Application logging initialized')

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views'))


app.config.from_object(Config)

# تهيئة قاعدة البيانات
db = SQLAlchemy(app)

# استيراد المتحكمات والمسارات
from app.controllers import product_controller, cart_controller, order_controller
from app import routes
