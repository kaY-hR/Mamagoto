from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pickle, os
from . import common
from dbio import MailIO

mails_bp = Blueprint('mails', __name__)

class MailsPage:
    query_dict = {}
    mail_data = None
    column_names = None

    def render_mails():
        return render_template(
            "mails.html",
            mails=MailsPage.mail_data,
            column_names=MailsPage.column_names,
            query_names=MailsPage.query_dict.keys(),
        )

    @staticmethod
    def save_query_pickle():
        with open(common.MAILS_SAVED_QUERY_PICKLE_PATH, "wb") as file:
            pickle.dump(MailsPage.query_dict, file)

    @staticmethod
    def load_query_pickle():
        if os.path.exists(common.MAILS_SAVED_QUERY_PICKLE_PATH):
            with open(common.MAILS_SAVED_QUERY_PICKLE_PATH, "rb") as file:
                MailsPage.query_dict = pickle.load(file)

    @mails_bp.route("/mails", methods=["GET", "POST"])
    def mails():
        MailsPage.load_query_pickle()
        return MailsPage.render_mails()

    @mails_bp.route("/mails-save-query", methods=["POST"])
    def save_query():
        query_name = request.form.get("query_name")
        sql = request.form.get("sql")
        if query_name and sql:
            MailsPage.query_dict[query_name] = sql
            MailsPage.save_query_pickle()
        return MailsPage.render_mails()

    @mails_bp.route("/mails-execute-saved-query", methods=["POST"])
    def execute_saved_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in MailsPage.query_dict:
            sql = MailsPage.query_dict[selected_query_name]
            MailsPage.mail_data, MailsPage.column_names = MailIO.exec_sql(sql)
        return MailsPage.render_mails()

    @mails_bp.route("/mails-delete-query", methods=["POST"])
    def delete_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in MailsPage.query_dict:
            del MailsPage.query_dict[selected_query_name]
            MailsPage.save_query_pickle()
        return MailsPage.render_mails()