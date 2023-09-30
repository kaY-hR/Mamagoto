from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pickle, os
import common
import dbio

logs_bp = Blueprint('logs', __name__)

class LogsPage:
    query_dict = {}
    log_data = None
    column_names = None

    def render_logs():
        return render_template(
            "logs.html",
            logs=LogsPage.log_data,
            column_names=LogsPage.column_names,
            query_names=LogsPage.query_dict.keys(),
        )

    @staticmethod
    def save_query_pickle():
        with open(common.LOGS_SAVED_QUERY_PICKLE_PATH, "wb") as file:
            pickle.dump(LogsPage.query_dict, file)

    @staticmethod
    def load_query_pickle():
        if os.path.exists(common.LOGS_SAVED_QUERY_PICKLE_PATH):
            with open(common.LOGS_SAVED_QUERY_PICKLE_PATH, "rb") as file:
                LogsPage.query_dict = pickle.load(file)

    @logs_bp.route("/logs", methods=["GET", "POST"])
    def logs():
        LogsPage.load_query_pickle()
        return LogsPage.render_logs()

    @logs_bp.route("/logs-save-query", methods=["POST"])
    def save_query():
        query_name = request.form.get("query_name")
        sql = request.form.get("sql")
        if query_name and sql:
            LogsPage.query_dict[query_name] = sql
            LogsPage.save_query_pickle()
        return LogsPage.render_logs()

    @logs_bp.route("/logs-execute-saved-query", methods=["POST"])
    def execute_saved_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in LogsPage.query_dict:
            sql = LogsPage.query_dict[selected_query_name]
            LogsPage.log_data, LogsPage.column_names = dbio.LogIO.exec_sql(sql)
        return LogsPage.render_logs()

    @logs_bp.route("/logs-delete-query", methods=["POST"])
    def delete_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in LogsPage.query_dict:
            del LogsPage.query_dict[selected_query_name]
            LogsPage.save_query_pickle()
        return LogsPage.render_logs()