import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key'  # مفتاح سري لتأمين الجلسات
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ecommerce.db')  # قاعدة البيانات
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # تعطيل تعديلات SQLAlchemy