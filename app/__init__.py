from flask import Flask
from .database import engine, Base
from .routes.books_bp import blueprint as book_blueprint
from .routes.issuance_bp import blueprint as issuance_blueprint
from .routes.publisher_bp import blueprint as publisher_blueprint
from .routes.reader_bp import blueprint as reader_blueprint
from .routes.generate_report import blueprint as report_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    Base.metadata.create_all(bind=engine)

    app.register_blueprint(book_blueprint, url_prefix="/api")
    app.register_blueprint(issuance_blueprint, url_prefix="/api")
    app.register_blueprint(publisher_blueprint, url_prefix="/api")
    app.register_blueprint(reader_blueprint, url_prefix="/api")
    app.register_blueprint(report_blueprint, url_prefix="/api")
    return app
