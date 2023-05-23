import datetime
import decimal
import json
import os

from flask import current_app as app, url_for
from flask_babel import gettext

from app.models.db import get_db, t_report_definition


def create_album_report_template():
    # use a predefined report definition so you don't have to start from scratch in this demo app,
    # for a real word app you would probably start with an empty report if nothing was saved previously

    with open(os.path.join(app.static_folder, 'report_definition.json')) as json_file:
        report_definition = json.load(json_file)

    db_engine = get_db()
    with db_engine.begin() as connection:
        connection.execute(
            t_report_definition.insert()
            .values(
                report_type='albums_report', report_definition=report_definition,
                last_modified_at=datetime.datetime.now()
            )
        )


def get_menu_items(controller):
    """Returns application menu items with special class for active menu item."""
    return (
        {'url': url_for('album.index'), 'label': gettext('menu.albums'),
         'id': 'menu_album', 'class': 'activeMenuItem' if controller == 'album' else ''},
        {'url': url_for('report.edit'), 'label': gettext('menu.report'),
         'id': 'menu_report', 'class': 'activeMenuItem' if controller == 'report' else ''})


def json_default(obj):
    """Serializes decimal and date values, can be used for json encoder."""
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, datetime.date):
        return str(obj)
    raise TypeError
