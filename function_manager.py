import json
import os
import tools
from dbio import MailIO, StructureIO
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import virtual_employee.staff
STORAGE_PATH = '.\\storage\\'
COMMON_STORAGE_PATH = STORAGE_PATH + 'common\\'


class FunctionManager:
    functions = [
        {
            "name": "save_file",
            "description": "Save a text file on private/shared storage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "FilePath": {
                        "type": "string",
                        "description": "the path for the file to save. DO NOT put a leading backslash, and MUST USE DOUBLE BACKSLASH INSTEAD OF SLASH",
                    },
                    "ForShared": {
                        "type": "boolean",
                        "description": "Set True to save the file to SHARED STORAGE so that your colleagues can see it.",
                    },
                    "Content": {
                        "type":"string",
                        "description":"Write the content to save."
                    }
                },
                "required": ["FilePath", "ForShared", "Content"],
            },
        },
        {
            "name": "read_file",
            "description": "Read a text file on private/shared storage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "FilePath": {
                        "type": "string",
                        "description": "the path for the file to read. DO NOT put a leading backslash, and MUST USE DOUBLE BACKSLASH INSTEAD OF SLASH",
                    },
                    "ForShared": {
                        "type": "boolean",
                        "description": "If the file is shared, set True. If the file is your private file, set False.",
                    },
                },
                "required": ["FilePath", "ForShared"],
            },
        },
        {
            "name": "list_storage",
            "description": "Look private/shared storage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "LookSharedStorage": {
                        "type": "boolean",
                        "description": "If you want to look shared storage, set True. If you want to look your private storage, set False",
                    },
                },
                "required": ["LookSharedStorage"],
            },
        },
        {
            "name": "send_mail",
            "description": "Send an email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "To": {
                        "type": "string",
                        "description": "Set the name to send to an individual or the department name to send to the entire department.",
                    },
                    "Content": {
                        "type": "string",
                        "description": "Email content.",
                    }
                },
                "required": ["To", "Content"],
            },
        },
        {
            "name": "get_new_mails",
            "description": "Get a list of new emails.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        {
            "name": "wait_others_action",
            "description": "Waiting for others to take action because the tasks have been digested",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
        {
            "name": "get_address_book",
            "description": "Get a list of employees' names and departments' name.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    ]

    @staticmethod
    def get_required_params(func_name: str):
        for func in FunctionManager.functions:
            if func["name"] == func_name:
                return func["parameters"]["required"]
        return []
    
    @staticmethod
    def get_boolean_params(func_name:str):
        for func in FunctionManager.functions:
            if func["name"] == func_name:
                return [key for key,value in func["parameters"]["properties"].items() if value["type"]=="boolean"]
        else:
            return []

    @staticmethod
    def exec_func(func_name: str, args: json, staff:'virtual_employee.staff.Staff'):
        function_message = None
        for func in FunctionManager.functions:
            if func["name"] == func_name:
                function_message = FunctionManager.call_function(func, args, staff)
                break
        else:
            function_message = "ERROR: USE ONLY THE FUNCTIONS PROVIDED"

        print(f"func_name:{func_name}, args:{str(args)}")

        return {"role": "function", "name": func_name, "content": function_message}

    @staticmethod
    def call_function(func, json_data: json, staff:'virtual_employee.staff.Staff'):
        func_name = func["name"]
        error_message = FunctionManager.validate_json(json_data=json_data, func_name=func["name"])
        if error_message:
            return error_message + FunctionManager.generate_format_explanation(func)

        if func_name == "save_file":
            return FunctionManager.save_file(json_data, staff.name)
        elif func_name == "read_file":
            return FunctionManager.read_file(json_data, staff.name)
        elif func_name == "list_storage":
            return FunctionManager.list_dir(json_data, staff.name)
        elif func_name == "send_mail":
            return FunctionManager.send_mail(json_data, staff.name)
        elif func_name == "get_new_mails":
            return FunctionManager.get_new_mails(staff.name, staff.time_checked_mails)
        elif func_name == "wait_others_action":
            return FunctionManager.wait_others_action(staff)
        elif func_name == "get_address_book":
            return FunctionManager.get_address_book()

    @staticmethod
    def get_dir(common: bool, name: str):
        file_dir = (
            COMMON_STORAGE_PATH
            if common
            else STORAGE_PATH + f"{name}\\"
        )
        return file_dir

    @staticmethod
    def validate_json(json_data: json, func_name:str):
        error_message = None
        for key in FunctionManager.get_required_params(func_name):
            if key not in json_data:
                error_message = f"Your json does not contain '{key}' key. "
                break

        for key in FunctionManager.get_boolean_params(func_name):
            if key in json_data and not isinstance(json_data[key], bool):
                error_message = f"Your json's '{key}' value is not boolean. "
                break

        return error_message

    @staticmethod
    def generate_format_explanation(func):
        description = func["description"]
        parameters = func["parameters"]["properties"]
        explanation = [f"{description}\n"]
        for param, param_info in parameters.items():
            explanation.append(f"{param}: {param_info['description']}")
        return "\n".join(explanation)

    @staticmethod
    def save_file(json_data: json, name: str):
        try:
            dir_path = FunctionManager.get_dir(json_data["ForShared"], name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(
                os.path.join(dir_path, json_data["FilePath"]),
                "w+",
                encoding="utf-8",
            ) as file:
                file.write(json_data["Content"])
        except:
            return (
                "An error has occurred. Please check if the parameters are appropriate."
            )

        return "Succeeded Saving File."

    @staticmethod
    def read_file(json_data: json, name: str):
        try:
            with open(
                os.path.join(FunctionManager.get_dir(json_data["ForShared"], name), json_data["FilePath"]),
                "r",
                encoding="utf-8",
            ) as file:
                return file.read()
        except:
            return f"{json_data['FilePath']} does not exist."

    @staticmethod
    def list_dir(json_data: json, name: str):
        dir_path = FunctionManager.get_dir(json_data["LookSharedStorage"], name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        result = tools.print_directory_structure(dir_path)

        return result if result else "empty"
    
    @staticmethod
    def send_mail(json_data:json, name:str):
        MailIO.send_mail(name, json_data["To"], json_data["Content"])
        return "Message sent successfully."
    
    @staticmethod
    def get_new_mails(name:str, time:datetime):
        raw_data = MailIO.get_new_mails(name,time)
        return str([str(raw_mail) for raw_mail in raw_data])
    
    @staticmethod
    def wait_others_action(staff:'virtual_employee.staff.Staff'):
        staff.deactivate()
        return "Waiting..."
    
    @staticmethod
    def get_address_book():
        try:
            return MailIO.get_address_book()
        except Exception as e:
            return f"An error occurred while getting the address book: {str(e)}"