import datetime
import json

from flask import Blueprint, Response, abort, current_app as app, redirect, render_template, request, url_for
from flask_babel import gettext
from sqlalchemy import func, select

from app.models.db import get_db, t_album, t_report_definition
from app.models.utils import create_album_report_template, get_menu_items, json_default

album_bp = Blueprint('album', __name__, url_prefix='/album')


@album_bp.route('/data/')
def data():
    """Returns available albums from the database. Can be optionally filtered by year.

    This is called from templates/album/index.html when the year input is changed.
    """
    year = request.args.get('year')
    if year:
        try:
            year = int(year)
        except (ValueError, TypeError):
            abort(400, 'invalid year parameter')
    else:
        year = None
    return json.dumps(get_albums(year), default=json_default)


@album_bp.route('/edit/')
@album_bp.route('/edit/<int:album_id>')
def edit(album_id=None):
    """Shows an edit form to add new or edit an existing album."""
    db_engine = get_db()
    rv = dict()
    rv['menu_items'] = get_menu_items('album')
    if album_id:
        with db_engine.begin() as connection:
            album = connection.execute(
                select(t_album)
                .where(t_album.c.id == album_id)
            ).fetchone()
        if not album:
            redirect(url_for('album.index'))
        rv['is_new'] = False
        rv['album'] = json.dumps(dict(
            id=album.id, name=album.name, artist=album.artist, year=album.year,
            best_of_compilation=album.best_of_compilation,
        ))
    else:
        rv['is_new'] = True
        rv['album'] = json.dumps(dict(id='', name='', year=None, best_of_compilation=False))
    return render_template('album/edit.html', **rv)


@album_bp.route('/')
@album_bp.route('/index')
def index():
    """Shows a page where all available albums are listed."""
    rv = dict()
    rv['menu_items'] = get_menu_items('album')
    rv['albums'] = json.dumps(get_albums(), default=json_default)
    return render_template('album/index.html', **rv)


@album_bp.route('/report/')
def report():
    """Prints a pdf file with all available albums.

    The albums can be optionally filtered by year. reportbro-lib is used to
    generate the pdf file. The data itself is retrieved
    from the database (*get_albums*). The report_definition
    is also stored in the database and is created on-the-fly if not present (to make
    this Demo App easier to use).
    """
    from reportbro import Report, ReportBroError

    year = request.args.get('year')
    if year:
        try:
            year = int(year)
        except (ValueError, TypeError):
            abort(400, 'invalid year parameter')
    else:
        year = None

    db_engine = get_db()

    # NOTE: these params must match exactly with the parameters defined in the
    # report definition in ReportBro Designer, check the name and type (Number, Date, List, ...)
    # of those parameters in the Designer.
    params = dict(year=year, albums=get_albums(year), current_date=datetime.datetime.now())

    with db_engine.begin() as connection:
        report_count = connection.execute(
            select(func.count(t_report_definition.c.id))
            .where(t_report_definition.c.report_type == 'albums_report')
        ).scalar()
        if report_count == 0:
            create_album_report_template()

        report_definition = connection.execute(
            select(t_report_definition.c.id, t_report_definition.c.report_definition)
            .where(t_report_definition.c.report_type == 'albums_report')
        ).fetchone()
        if not report_definition:
            raise abort(500, 'no report_definition available')

    try:
        report_inst = Report(report_definition.report_definition, params)
        if report_inst.errors:
            # report definition should never contain any errors,
            # unless you saved an invalid report and didn't test in ReportBro Designer
            raise ReportBroError(report_inst.errors[0])

        pdf_report = report_inst.generate_pdf()
        response = Response()
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename="albums.pdf"'
        response.set_data(bytes(pdf_report))
        return response
    except ReportBroError as ex:
        app.logger.error(ex.error)
        abort(500, 'report error: ' + str(ex.error))
    except Exception as ex:
        abort(500, 'report exception: ' + str(ex))


@album_bp.route('/save',  methods=['POST'])
def save():
    """Saves a music album in the db."""
    db_engine = get_db()
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'invalid request values')
    album = json_data.get('album')
    if not isinstance(album, dict):
        abort(400, 'invalid values')
    album_id = None
    if album.get('id'):
        try:
            album_id = int(album.get('id'))
        except (ValueError, TypeError):
            abort(400, 'invalid album id')

    values = dict(best_of_compilation=album.get('best_of_compilation'))
    rv = dict(errors=[])

    # perform some basic form validation
    if not album.get('name'):
        rv['errors'].append(dict(field='name', msg=str(gettext('error.the field must not be empty'))))
    else:
        values['name'] = album.get('name')
    if not album.get('artist'):
        rv['errors'].append(dict(field='artist', msg=str(gettext('error.the field must not be empty'))))
    else:
        values['artist'] = album.get('artist')
    if album.get('year'):
        try:
            values['year'] = int(album.get('year'))
            if values['year'] < 1900 or values['year'] > 2100:
                rv['errors'].append(dict(field='year', msg=str(gettext('error.the field must contain a valid year'))))
        except (ValueError, TypeError):
            rv['errors'].append(dict(field='year', msg=str(gettext('error.the field must contain a number'))))
    else:
        values['year'] = None

    if not rv['errors']:
        # no validation errors -> save album
        with db_engine.begin() as connection:
            if album_id:
                connection.execute(
                    t_album.update()
                    .where(t_album.c.id == album_id)
                    .values(**values)
                )
            else:
                connection.execute(
                    t_album.insert()
                    .values(**values)
                )
    return json.dumps(rv)


def get_albums(year=None):
    """Returns available albums from the database. Can be optionally filtered by year."""
    db_engine = get_db()
    select_albums = select(t_album)
    if year is not None:
        select_albums = select_albums.where(t_album.c.year == year)
    items = []
    with db_engine.begin() as connection:
        rows = connection.execute(select_albums).fetchall()
        for row in rows:
            items.append(dict(
                id=row.id, name=row.name, artist=row.artist, year=row.year,
                best_of_compilation=row.best_of_compilation,
            ))
    return items
