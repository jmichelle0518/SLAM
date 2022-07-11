import dash
from flask import Flask
from flask.helpers import get_root_path
from dash_extensions.enrich import DashProxy, ServersideOutputTransform
import os

from app.dashapp.callbacks import register_callbacks

def localize_asset_path(path):
    return os.environ.get('APP_ASSETS_PATH','/dashboard/assets/') + path

title = 'SLAM'
logo_src = localize_asset_path('NERDS-logo.svg')

def create_dev_app(**kwargs):
    from dashapp.layout import main_layout
    clear = kwargs.get('clear_cache',False)
    print(title)
    os.environ['APP_ASSETS_PATH'] = '/assets/'
    dashapp = _initialize_dash(server=True, pathname = '/')
    _setup_dash(dashapp, main_layout, title, flask=False)
    return dashapp

def create_app(**kwargs):
    server = Flask(__name__)
    server.secret_key = os.environ['SESSION_KEY']

    for key in kwargs:
        server.config[key] = kwargs[key]

    register_dashapp(server)
    register_blueprints(server)

    return server

def _initialize_dash(server=True, pathname='/dashboard/'):
    return DashProxy(__name__,
        server=server,
        url_base_pathname=pathname,
        assets_folder=get_root_path(__name__) + '/assets/',
        assets_ignore='.*-checkpoint\.css',
        transforms=[ServersideOutputTransform()]
        )

def _setup_dash(dashapp, layout, title, flask=True):
    dashapp.title = title
    dashapp.layout = layout
    dashapp.config['suppress_callback_exceptions'] = True
    register_callbacks(dashapp, flask=flask)

def register_dashapp(app):
    from dash import html, dcc
    from dash.dependencies import Input, Output, State
    from dashapp.layout import main_layout

    print(title)
    dashapp = _initialize_dash(app)

    with app.app_context():
        _setup_dash(dashapp, main_layout, title)

def register_blueprints(server):
    from app.webapp import server_bp

    server .register_blueprint(server_bp)
