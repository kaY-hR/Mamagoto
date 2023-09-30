import openaiIO
from WebUIServer import flaskserver, common
import webbrowser
import threading, pickle, os, time
from dbio import LogIO,MailIO,StructureIO,DepartmentIO
import os
import shutil
from function_manager import STORAGE_PATH
from virtual_employee.staff import Staff

def run_server():
    flaskserver.FlaskServer.app.run(debug=False, host="127.0.0.1", port=5000)


def main():
    webbrowser.open("http://127.0.0.1:5000")
    openaiIO.openaiIO.init_openai()

    while True:
        if MailIO.exist_any_mails():
            for staff in Staff.staff_list.values():
                if not(staff.is_active):
                    staff.activate()
        else:
            time.sleep(3)

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


if __name__ == "__main__":
    if os.path.isfile(common.DB_PATH):
        os.remove(common.DB_PATH)
        
    init_storage()

    LogIO.create_log_table()
    MailIO.create_mail_table()
    StructureIO.create_structure_table()
    DepartmentIO.create_department_table()

    # スレッドを作成して実行
    thread_server = threading.Thread(target=run_server)
    thread_main = threading.Thread(target=main)

    # スレッドを開始
    thread_server.start()
    thread_main.start()

    thread_server.join()
    thread_main.join()
