from flask import Blueprint, redirect, render_template, request, url_for, session
import os

USER_KEY = "";
SESSION_USER = "";
EMAIL_KEY = "";
SESSION_EMAIL = "";

server_bp = Blueprint("main",__name__)

admin_emails = ['']

@server_bp.route("/")
def index():
    rqst = request.headers
    if USER_KEY in rqst:
        uname = rqst[USER_KEY]
        session[SESSION_USER] = uname
    username = session[SESSION_USER]
    return redirect(url_for("/dashboard/",_scheme="https",_external=True))
