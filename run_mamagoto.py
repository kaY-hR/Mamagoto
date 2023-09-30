import os, time
from dbio import LogIO,MailIO,StructureIO,DepartmentIO
import os
import shutil
from function_manager import STORAGE_PATH
from virtual_employee.staff import Staff
import common

def init_storage():
    directory_to_clean = STORAGE_PATH

    for filename in os.listdir(directory_to_clean):
        file_path = os.path.join(directory_to_clean, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'削除エラー: {e}')

    # commonフォルダを作成
    common_folder = os.path.join(directory_to_clean, 'common')
    os.makedirs(common_folder)

def init_database():
    if os.path.isfile(common.DB_PATH):
        os.remove(common.DB_PATH)
    LogIO.create_log_table()
    MailIO.create_mail_table()
    StructureIO.create_structure_table()
    DepartmentIO.create_department_table() 

def run_mamagoto():
    while True:
        if MailIO.exist_any_mails():
            for staff in Staff.staff_list.values():
                if not(staff.is_active):
                    staff.activate()
        else:
            time.sleep(3)

if __name__ == "__main__":
    init_storage()
    init_database()
    run_mamagoto()