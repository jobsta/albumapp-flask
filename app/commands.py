import os
import click
from flask.cli import AppGroup

db_cli = AppGroup('db')
translate_cli = AppGroup('translate')


@db_cli.command('create')
def create_db():
    import app.models.db as db
    db.init_db()


@translate_cli.command('init')
@click.argument('lang', default='en_GB')
def init_language(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate_cli.command('update')
def update_languages():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate_cli.command('compile')
def compile_languages():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')
