from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pickle, os
import common
from virtual_employee.staff import Staff
from virtual_employee.softbots import PersonalityGenerator
from dbio import DepartmentIO, StructureIO
from .tools import read_md
import csv
import io

employee_bp = Blueprint("employee-page", __name__)

@employee_bp.route("/employee-page", methods=["GET", "POST"])
def employee_page():
    StructurePage.load_query_pickle()
    departments, _ = DepartmentIO.get_all_departments()
    md = read_md("employee_registration")
    return render_template(
        "employee_registration.html",
        md=md,
        departments=departments,
        employees=StructurePage.employee_data,
        column_names=StructurePage.column_names,
        query_names=StructurePage.query_dict.keys(),
    )


class RegistrationPage:

    @employee_bp.route("/employee-page/register", methods=["POST"])
    def register():
        #staff = Staff(PersonalityGenerator.generate_personality_traits())
        staff = Staff()
        selected_departments = request.form.getlist("departments")
        StructureIO.insert_employee_departments(staff.name, selected_departments)

        init_instructions = request.form.get("requirements")
        staff.add_instructions(
            "You are the person who meets the following requirements:"
            + init_instructions
        )

        for department in selected_departments:
            mission = DepartmentIO.get_mission_by_name(department)
            staff.add_instructions(f"You belong to the {department} Department. The mission of this department is:\n{mission}")

        staff.activate()
        return employee_page()
    
    @employee_bp.route("/employee-page/load-csv", methods=["POST"])
    def load_csv():
        filebuf = request.files.get('csv_file')
        text_stream = io.TextIOWrapper(filebuf, encoding='utf-8')
        for row in csv.reader(text_stream):
            staff = Staff()
            departments = row[0].split('\n')
            staff.add_instructions(
                "You are the person who meets the following requirements:"
                + row[1]
            )
            for department in departments:
                mission = DepartmentIO.get_mission_by_name(department)
                staff.add_instructions(f"You belong to the {department} Department. The mission of this department is:\n{mission}")
            staff.activate()
            StructureIO.insert_employee_departments(staff.name, departments)
        
        return employee_page()

class StructurePage:
    query_dict = {}
    employee_data = None
    column_names = None

    @staticmethod
    def save_query_pickle():
        with open(common.STRUCTURE_SAVED_QUERY_PICKLE_PATH, "wb") as file:
            pickle.dump(StructurePage.query_dict, file)

    @staticmethod
    def load_query_pickle():
        if os.path.exists(common.STRUCTURE_SAVED_QUERY_PICKLE_PATH):
            with open(common.STRUCTURE_SAVED_QUERY_PICKLE_PATH, "rb") as file:
                StructurePage.query_dict = pickle.load(file)

    @employee_bp.route("/employee-page/structure-save-query", methods=["POST"])
    def save_query():
        query_name = request.form.get("query_name")
        sql = request.form.get("sql")
        if query_name and sql:
            StructurePage.query_dict[query_name] = sql
            StructurePage.save_query_pickle()
        return employee_page()

    @employee_bp.route("/employee-page/structure-execute-saved-query", methods=["POST"])
    def execute_saved_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in StructurePage.query_dict:
            sql = StructurePage.query_dict[selected_query_name]
            (
                StructurePage.employee_data,
                StructurePage.column_names,
            ) = StructureIO.exec_sql(sql)
        return employee_page()

    @employee_bp.route("/employee-page/structure-delete-query", methods=["POST"])
    def delete_query():
        selected_query_name = request.form.get("selected_query_name")
        if selected_query_name in StructurePage.query_dict:
            del StructurePage.query_dict[selected_query_name]
            StructurePage.save_query_pickle()
        return employee_page()
