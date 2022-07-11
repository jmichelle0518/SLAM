#import base64                                   # file contents conversion
import os                                       # helps with directory management for saving and serving files
import dash
import dash_bootstrap_components as dbc

from dashapp.layout import serve_layout
from dashapp.callbacks import register_callbacks

from flask import Flask, send_from_directory    # custom app server configuration for file downloads
from flask.helpers import get_root_path
#import copy                                     # managing copied text from Document runs
#from docx2python import docx2python             # reading word documents as text
#import docx                                     # building word documents and saving them out as files
#from docx import Document                       # object holding the word document and its styling
#from dash.dependencies import Input, Output
#from datetime import datetime as dt

UPLOAD_DIRECTORY = "/app/app_uploaded_files"         # folder for uploads to live, eventually, only temporarily

if not os.path.exists(UPLOAD_DIRECTORY):        # if the folder doesn't exist, make it
    os.makedirs(UPLOAD_DIRECTORY)

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:

app = dash.Dash(__name__, assets_folder = get_root_path(__name__)+'/assets/', external_stylesheets=[dbc.themes.SUPERHERO])
app.title = "SLAM"
app.layout = serve_layout()
register_callbacks(app)

def create_app(**kwargs):
    server = Flask(__name__)
    server.secret_key = os.environ["SESSION_KEY"]

    @server.route("/")
    def dashboard():
        return app.index()

# for debugging
if __name__ == '__main__':
    app.run_server(debug=True)
