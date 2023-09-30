from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pickle, os
from . import common
from virtual_employee.staff import Staff
from virtual_employee.softbots import PersonalityGenerator
from dbio import MailIO,StructureIO
from .tools import read_md

send_mail_bp = Blueprint('send-mail-page', __name__)

class SendMailPage:

    @send_mail_bp.route("/send-mail-page", methods=["GET", "POST"])
    def send_mail():
        if request.method == "POST":
            addresses = request.form.getlist("address")
            content = request.form["content"]
            for address in addresses:
                MailIO.send_mail("President",address,content)
        return render_template("send_mail.html", addresses= StructureIO.get_employee_department_list(), md = read_md("send_mail"))
