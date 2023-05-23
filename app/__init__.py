__version__ = "1.0.0"

from flask import Flask, redirect, url_for
from flask_babel import Babel
from .commands import db_cli, translate_cli
from app.models import db
from app.models.errorhandlers import register_handlers
import logging
import os


def configure_logger():
    from logging.config import dictConfig

    log_path = os.path.join('instance', 'log')

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '%(asctime)s %(levelname)s in %(filename)s:%(lineno)d: %(message)s',
        }},
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_path, 'albumapp.log'),
                'maxBytes': 5000000,
                'backupCount': 3
            },
            'console': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream'
            },
            'error': {
                'formatter': 'default',
                'class': 'logging.FileHandler',
                'filename': os.path.join(log_path, 'error.log'),
            },
        },
        'root': {
            'level': 'INFO',
            'handlers': ['default', 'console']
        }
    })


def cleanup(e=None):
    db.close_db(e)


def get_locale():
    return 'en_GB'


def create_app():
    # configure logger before logger is accessed
    configure_logger()

    app = Flask(__name__, instance_relative_config=True)
    Babel(app, locale_selector=get_locale)

    # load config from instance/config.py
    app.config.from_pyfile('config.py')

    if app.debug:
        app.logger.setLevel(logging.DEBUG)
        app.logger.debug('running in DEBUG mode')
    else:
        # log errors into separate file so they can be detected by monitoring
        file_handler = logging.FileHandler(os.path.join('instance/log', 'error.log'))
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

    from app.views.album import album_bp
    from app.views.home import home_bp
    from app.views.report import report_bp

    app.register_blueprint(album_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(report_bp)
    app.teardown_appcontext(cleanup)

    register_handlers(app)
    app.cli.add_command(db_cli)
    app.cli.add_command(translate_cli)

    @app.route('/')
    def index():
        return redirect(url_for('home.index'))

    return app

