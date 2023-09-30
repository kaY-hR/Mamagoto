from flask import Flask, render_template, request, redirect, url_for
import pickle, os
from . import common
from .logs import logs_bp
from .mails import mails_bp
from .employee_registration import employee_bp
from .departments import departments_bp
from .tools import read_md

class FlaskServer:
    app = Flask(__name__)
    app.register_blueprint(logs_bp)
    app.register_blueprint(mails_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(departments_bp)

    @app.route("/", methods=["GET", "POST"])
    def index():
        content = read_md("index")
        return render_template("index.html",content = content)
