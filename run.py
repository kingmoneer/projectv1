import logging
from app import app, db

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Starting application")
    try:
        with app.app_context():
            logger.info("Creating database tables")
            db.create_all()
        logger.info("Database tables created successfully")
        app.run(debug=True)
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        raise
