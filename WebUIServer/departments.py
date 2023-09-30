from flask import Blueprint, render_template, request, redirect, url_for
from dbio import StructureIO, DepartmentIO
from .tools import read_md

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

    @departments_bp.route("/departments/edit-department", methods=["POST"])
    def edit_department():
        selected_department_id = int(request.form.get("selected_department"))
        new_name = request.form.get("new_name")
        new_mission = request.form.get("new_mission")
        if new_name and new_mission:
            DepartmentIO.update_department(selected_department_id, new_name, new_mission)
        return redirect(url_for("departments.departments"))

