from flask import g, current_app as app
from sqlalchemy import create_engine
from sqlalchemy import Boolean, BLOB, JSON, Table, Column, DateTime, Integer, String, Text, MetaData


metadata = MetaData()

# store report requests for testing, used by ReportBro Designer
# for preview of pdf and xlsx
t_report_request = Table(
    'report_request', metadata,
    Column('id', Integer, primary_key=True),
    Column('key', String(36), nullable=False),
    Column('report_definition', Text, nullable=False),
    Column('data', Text, nullable=False),
    Column('is_test_data', Boolean, nullable=False),
    Column('pdf_file', BLOB),
    Column('pdf_file_size', Integer),
    Column('created_on', DateTime, nullable=False))

# report definition for our album report which is used for printing
# the pdf with the album list. When the report is saved
# in ReportBro Designer it will be stored in this table.
t_report_definition = Table(
    'report_definition', metadata,
    Column('id', Integer, primary_key=True),
    Column('report_definition', JSON, nullable=False),
    Column('report_type', String(30), nullable=False),
    Column('remark', Text),
    Column('last_modified_at', DateTime, nullable=False))

# application data which can be added and edited in a form
t_album = Table(
    'album', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('artist', String(100), nullable=False),
    Column('year', Integer),
    Column('best_of_compilation', Boolean, nullable=False, default=False))


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        engine = create_engine(app.config['DATABASE_URL'])
        g.db = engine
    return g.db


def close_db(e=None):
    g.pop('db', None)


def init_db():
    engine = create_engine(app.config['DATABASE_URL'])
    metadata.create_all(engine)
