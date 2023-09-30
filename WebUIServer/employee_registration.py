from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for
import pickle, os
from . import common
from virtual_employee.staff import Staff
from virtual_employee.softbots import PersonalityGenerator
from dbio import DepartmentIO,StructureIO
from .tools import read_md

register_bp = Blueprint('registration-page', __name__)

class RegistrationPage:

    @staticmethod
    def render_registratoin_page():
        departments,_ = DepartmentIO.get_all_departments()
        md = read_md("employee_registration")
        return render_template("employee_registration.html",md=md, departments=departments)

    @register_bp.route("/registration-page", methods=["GET", "POST"])
    def registration_page():
        return RegistrationPage.render_registratoin_page()
    
    @register_bp.route("/register-page-register", methods=["POST"])
    def register():
        staff = Staff(PersonalityGenerator.generate_personality_traits())
        selected_departments = request.form.getlist("departments")
        StructureIO.insert_employee_departments(staff.name, selected_departments)

        init_instructions = request.form.get("requirements")
        staff.add_instructions("You are the person who meets the following requirements:" + init_instructions)

        staff.activate()

        return RegistrationPage.render_registratoin_page()
