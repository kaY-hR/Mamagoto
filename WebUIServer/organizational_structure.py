from flask import Blueprint, render_template, request
from dbio import StructureIO
from . import common
import pickle, os


structure_bp = Blueprint('structure', __name__)

class StructurePage:
    query_dict = {}
    employee_data = None
    column_names = None

    def render_structure():
        return render_template(
            "structure.html",
            employees=StructurePage.employee_data,
            column_names=StructurePage.column_names,
            query_names=StructurePage.query_dict.keys(),
        )

    @staticmethod
    def save_query_pickle():
        with open(common.STRUCTURE_SAVED_QUERY_PICKLE_PATH, "wb") as file:
            pickle.dump(StructurePage.query_dict, file)

    @staticmethod
    def load_query_pickle():
        if os.path.exists(common.STRUCTURE_SAVED_QUERY_PICKLE_PATH):
            with open(common.STRUCTURE_SAVED_QUERY_PICKLE_PATH, "rb") as file:
                StructurePage.query_dict = pickle.load(file)

    @structure_bp.route("/structure", methods=["GET", "POST"])
    def structure():
        StructurePage.load_query_pickle()
        return StructurePage.render_structure()

    @structure_bp.route("/structure-save-query", methods=["POST"])
    def save_query():
        query_name = request.form.get("query_name")
        sql = request.form.get("sql")
        if query_name and sql:
            StructurePage.query_dict[query_name] = sql
            StructurePage.save_query_pickle()
        return StructurePage.render_structure()

    @structure_bp.route("/structure-execute-saved-query", methods=["POST"])
    def execute_saved_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in StructurePage.query_dict:
            sql = StructurePage.query_dict[selected_query_name]
            StructurePage.employee_data, StructurePage.column_names = StructureIO.exec_sql(sql)
        return StructurePage.render_structure()

    @structure_bp.route("/structure-delete-query", methods=["POST"])
    def delete_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in StructurePage.query_dict:
            del StructurePage.query_dict[selected_query_name]
            StructurePage.save_query_pickle()
        return StructurePage.render_structure()
