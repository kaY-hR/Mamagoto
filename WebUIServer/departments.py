from flask import Blueprint, render_template, request, redirect, url_for
from dbio import StructureIO, DepartmentIO
from .tools import read_md
import csv
import io

departments_bp = Blueprint('departments', __name__)

class DepartmentsPage:

    @departments_bp.route("/departments", methods=["GET"])
    def departments():
        departments, column_names = DepartmentIO.get_all_departments()
        md = read_md("departments")
        return render_template("departments.html",md=md, departments=departments, column_names = column_names)

    @departments_bp.route("/departments/add-department", methods=["POST"])
    def add_department():
        department_name = request.form.get("name")
        department_mission = request.form.get("mission")

        if department_name and department_mission:
            DepartmentIO.add_department(department_name, department_mission)
            print("部門が追加されました。")

        return redirect(url_for("departments.departments"))
    
    @departments_bp.route("/departments/load-csv", methods=["POST"])
    def load_csv():
        filebuf = request.files.get('csv_file')
        text_stream = io.TextIOWrapper(filebuf, encoding='utf-8')
        for row in csv.reader(text_stream):
            DepartmentIO.add_department(row[0], row[1])
        
        return redirect(url_for("departments.departments"))


