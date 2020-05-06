from flask import Blueprint, redirect, url_for

home_bp = Blueprint('home', __name__, url_prefix='/home')


@home_bp.route('/')
@home_bp.route('/index')
def index():
    return redirect(url_for('album.index'))
