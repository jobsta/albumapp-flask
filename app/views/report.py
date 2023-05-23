import datetime
import decimal
import json
import uuid

from flask import abort, Blueprint, render_template, Response, request
from reportbro import Report, ReportBroError
from sqlalchemy import func, select
from timeit import default_timer as timer

from app.models.db import get_db, t_report_definition, t_report_request
from app.models.utils import create_album_report_template, get_menu_items

report_bp = Blueprint('report', __name__, url_prefix='/report')

MAX_CACHE_SIZE = 1000 * 1024 * 1024  # keep max. 1000 MB of generated pdf files in sqlite db


@report_bp.route('/edit')
def edit():
    create_album_report_template()
    """Shows a page with ReportBro Designer to edit our albums report template.

    The report template is loaded from the db (report_definition table),
    in case no report template exists a hardcoded template is generated in
    *create_album_report_template* for this Demo App. Normally you'd probably
    start with an empty report (empty string, so no report is loaded
    in the Designer) in this case.
    """
    db_engine = get_db()
    rv = dict()
    rv['menu_items'] = get_menu_items('report')

    with db_engine.begin() as connection:
        report_count = connection.execute(
            select(func.count(t_report_definition.c.id))
            .where(t_report_definition.c.report_type == 'albums_report')
        ).scalar()
        if report_count == 0:
            create_album_report_template()

        # load ReportBro report definition stored in our report_definition table
        row = connection.execute(
            select(t_report_definition.c.id, t_report_definition.c.report_definition)
            .where(t_report_definition.c.report_type == 'albums_report')
        ).fetchone()

    rv['report_definition'] = json.dumps(row.report_definition)
    return render_template('report/edit.html', **rv)


@report_bp.route('/run', methods=['GET', 'PUT', 'OPTIONS'])
def run():
    """Generates a report for preview.

    This method is called by ReportBro Designer when the Preview button is clicked,
    the url is defined when initializing the Designer, see *reportServerUrl*
    in templates/report/edit.html
    """
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] =\
        'Origin, X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept, Authorization, Z-Key'
    if request.method == 'OPTIONS':
        # options request is usually sent by browser for a cross-site request, we only need to set the
        # Access-Control-Allow headers in the response so the browser sends the following get/put request
        return response

    additional_fonts = []
    # add additional fonts here if additional fonts are used in ReportBro Designer

    db_engine = get_db()
    with db_engine.begin() as connection:
        if request.method == 'PUT':
            # all data needed for report preview is sent in the initial PUT request, it contains
            # the format (pdf or xlsx), the report itself (report_definition), the data (test data
            # defined within parameters in the Designer) and is_test_data flag (always True
            # when request is sent from Designer)
            json_data = request.get_json(silent=True)
            if json_data is None:
                abort(400, 'invalid request')
            output_format = json_data.get('outputFormat')
            if output_format not in ('pdf', 'xlsx'):
                abort(400, 'outputFormat parameter missing or invalid')
            report_definition = json_data.get('report')
            data = json_data.get('data')
            is_test_data = bool(json_data.get('isTestData'))
            report = None
            try:
                report = Report(report_definition, data, is_test_data, additional_fonts=additional_fonts)
            except Exception as e:
                abort(400, 'failed to initialize report: ' + str(e))

            if report.errors:
                # return list of errors in case report contains errors, e.g. duplicate parameters.
                # with this information ReportBro Designer can select object containing errors,
                # highlight erroneous fields and display error messages
                response.set_data(json.dumps(dict(errors=report.errors), default=jsonconverter))
                return response
            try:
                now = datetime.datetime.now()

                # delete old reports (older than 3 minutes) to avoid table getting too big
                connection.execute(
                    t_report_request.delete()
                    .where(t_report_request.c.created_on < (now - datetime.timedelta(minutes=3)))
                )

                total_size = connection.execute(
                    select(func.sum(t_report_request.c.pdf_file_size))
                ).scalar()
                if total_size and total_size > MAX_CACHE_SIZE:
                    # delete all reports older than 10 seconds to reduce db size for cached pdf files
                    connection.execute(
                        t_report_request.delete()
                        .where(t_report_request.c.created_on < (now - datetime.timedelta(seconds=10)))
                    )

                start = timer()
                report_file = report.generate_pdf(add_watermark=True)
                end = timer()
                print('pdf generated in %.3f seconds' % (end-start))

                key = str(uuid.uuid4())
                # add report request into sqlite db, this enables downloading the report by url
                # (the report is identified by the key) without any post parameters.
                # This is needed for pdf and xlsx preview.
                connection.execute(
                    t_report_request.insert()
                    .values(
                        key=key, report_definition=json.dumps(report_definition),
                        data=json.dumps(data, default=jsonconverter), is_test_data=is_test_data,
                        pdf_file=report_file, pdf_file_size=len(report_file), created_on=now
                    )
                )
                response.set_data('key:' + key)
                return response
            except ReportBroError as err:
                # in case an error occurs during report generation a ReportBroError exception is thrown
                # to stop processing. We return this error within a list so the error can be
                # processed by ReportBro Designer.
                response.set_data(json.dumps(dict(errors=[err.error]), default=jsonconverter))
                return response

        elif request.method == 'GET':
            output_format = request.args.get('outputFormat')
            assert output_format in ('pdf', 'xlsx')
            key = request.args.get('key')
            report = None
            report_file = None
            if key and len(key) == 36:
                # the report is identified by a key which was saved
                # in an sqlite table during report preview with a PUT request
                row = connection.execute(
                    select(t_report_request)
                    .where(t_report_request.c.key == key)
                ).fetchone()
                if not row:
                    abort(400, 'report not found (preview probably too old), update report preview and try again')
                if output_format == 'pdf' and row.pdf_file:
                    report_file = row.pdf_file
                else:
                    report_definition = json.loads(row.report_definition)
                    data = json.loads(row.data)
                    is_test_data = row.is_test_data
                    report = Report(report_definition, data, is_test_data, additional_fonts=additional_fonts)
                    if report.errors:
                        abort(400, 'error generating report')
            else:
                # in case there is a GET request without a key we expect all report data to be available.
                # this is NOT used by ReportBro Designer and only added for the sake of completeness.
                json_data = request.get_json(silent=True)
                if json_data is None:
                    abort(400, 'invalid request')
                report_definition = json_data.get('report')
                data = json_data.get('data')
                is_test_data = bool(json_data.get('isTestData'))
                if not isinstance(report_definition, dict) or not isinstance(data, dict):
                    abort(400, 'report_definition or data missing')
                report = Report(report_definition, data, is_test_data, additional_fonts=additional_fonts)
                if report.errors:
                    abort(400, 'error generating report')

            try:
                # once we have the reportbro.Report instance we can generate
                # the report (pdf or xlsx) and return it
                now = datetime.datetime.now()
                if output_format == 'pdf':
                    if report_file is None:
                        # as it is currently implemented the pdf file is always stored in the
                        # report_request table along the other report data. Therefor report_file
                        # will always be set. The generate_pdf call here is only needed in case
                        # the code is changed to clear report_request.pdf_file column when the
                        # data in this table gets too big (currently whole table rows are deleted)
                        report_file = report.generate_pdf(add_watermark=True)

                    response.headers['Content-Type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = 'inline; filename="{filename}"'.format(
                        filename='report-' + str(now) + '.pdf')
                else:
                    report_file = report.generate_xlsx()
                    response.headers['Content-Type'] =\
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    response.headers['Content-Disposition'] = 'inline; filename="{filename}"'.format(
                        filename='report-' + str(now) + '.xlsx')
                response.set_data(report_file)
                return response
            except ReportBroError:
                abort(400, 'error generating report')
    return None


@report_bp.route('/save/<report_type>', methods=['PUT'])
def save(report_type):
    """Save report_definition in our db table.

    This method is called by save button in ReportBro Designer.
    The url is called in *saveReport* callback from the Designer,
    see *saveCallback* in templates/report/edit.html
    """
    db_engine = get_db()
    if report_type != 'albums_report':
        #  currently we only support the albums report
        abort(400, 'report_type not supported')
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'invalid request')
    report_definition = json_data.get('report')
    if not isinstance(report_definition, dict):
        abort(400, 'invalid request values')

    # perform some basic checks if all necessary fields for report_definition are present
    if 'docElements' not in report_definition or 'styles' not in report_definition or\
            'parameters' not in report_definition or\
            'documentProperties' not in report_definition or 'version' not in report_definition:
        abort(400, 'invalid request values')

    with db_engine.begin() as connection:
        report_count = connection.execute(
            select(func.count(t_report_definition.c.id))
            .where(t_report_definition.c.report_type == report_type)
        ).scalar()
        if report_count == 0:
            connection.execute(
                t_report_definition.insert()
                .values(
                    report_type=report_type, report_definition=report_definition,
                    last_modified_at=datetime.datetime.now()
                )
            )
        else:
            connection.execute(
                t_report_definition.update()
                .where(t_report_definition.c.report_type == report_type)
                .values(report_definition=report_definition, last_modified_at=datetime.datetime.now())
            )

    return json.dumps(dict(status='ok'))


def jsonconverter(val):
    """Handles json encoding of datetime and Decimal"""
    if isinstance(val, datetime.datetime):
        return '{date.year}-{date.month}-{date.day}'.format(date=val)
    if isinstance(val, decimal.Decimal):
        return str(val)
