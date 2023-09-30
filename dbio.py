import sqlite3
from WebUIServer import common
from datetime import datetime


class LogIO:
    @staticmethod
    def create_log_table():
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            # テーブルの作成とデータの挿入例
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS logs(
                    id INTEGER PRIMARY KEY,
                    Time DATETIME,
                    Speaker TEXT,
                    Listener TEXT,
                    Content TEXT
                )
            """
            )

            conn.commit()
            conn.close()
            print("データベースが作成されました。")
        except Exception as e:
            print(f"DB作成エラー: {e}")

    @staticmethod
    def add(speaker: str, listener: str, content: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO logs (Time, Speaker, Listener, Content) VALUES (?, ?, ?, ?)",
                (datetime.now(), speaker, listener, content),
            )

            conn.commit()
            conn.close()
            print("メッセージが追加されました。")
        except Exception as e:
            print(f"DB書込エラー: {e}")

    @staticmethod
    def exec_sql(sql: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()
            cursor.execute(sql)
            logs = cursor.fetchall()

            # カラム名を取得
            column_names = [desc[0] for desc in cursor.description]

            conn.commit()
            conn.close()

            return logs, column_names

        except Exception as e:
            print(f"DB SQL実行エラー: {e}")
            return None, None


class MailIO:
    @staticmethod
    def create_mail_table():
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS mails(
                    Time DATETIME,
                    From_ TEXT,
                    To_ TEXT,
                    Content TEXT
                )
            """
            )

            conn.commit()
            conn.close()
            print("Mail table has been created.")
        except Exception as e:
            print(f"Mail table creation error: {e}")

    @staticmethod
    def send_mail(from_: str, to: str, content: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO mails (Time, FROM_, TO_, Content) VALUES (?, ?, ?, ?)",
                (datetime.now(), from_, to, content),
            )

            conn.commit()
            conn.close()
            print("メールが送信されました。")
        except Exception as e:
            print(f"DB書込エラー: {e}")

    @staticmethod
    def get_mails(to: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            # Select emails for the specified recipient and their organization
            cursor.execute("""
                SELECT * FROM mails 
                WHERE (To_ = ? OR To_ = 'all') 
                OR To_ IN (SELECT DepartmentName FROM structure WHERE EmployeeName = ?)
            """, (to, to))
            mails = cursor.fetchall()

            conn.commit()
            conn.close()

            if mails:
                column_names = [desc[0] for desc in cursor.description]
                mails_dict_list = [dict(zip(column_names, mail)) for mail in mails]
                return mails_dict_list
            else:
                print("No emails found for the specified recipient.")
                return []

        except Exception as e:
            print(f"DB読込エラー: {e}")
            return []

    @staticmethod
    def get_new_mails(to: str, time: datetime = None):
        if not(time):
            return MailIO.get_mails(to)
        
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            # Select emails for the specified recipient and time, and their organization
            cursor.execute("""
                SELECT * FROM mails 
                WHERE (To_ = ? OR To_ = 'all') 
                OR (To_ IN (SELECT DepartmentName FROM structure WHERE EmployeeName = ?) AND Time >= ?)
            """, (to, to, time))
            mails = cursor.fetchall()

            conn.commit()
            conn.close()

            if mails:
                column_names = [desc[0] for desc in cursor.description]
                mails_dict_list = [dict(zip(column_names, mail)) for mail in mails]
                return mails_dict_list
            else:
                print("No new emails found for the specified recipient.")
                return []

        except Exception as e:
            print(f"DB読込エラー: {e}")
            return []
        
    @staticmethod
    def exist_any_mails():
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM mails")
            mails = cursor.fetchall()

            conn.commit()
            conn.close()

            if mails:
                return len(mails)>0
            else:
                print("No emails found.")
                return False

        except Exception as e:
            print(f"DB読込エラー: {e}")
            return False
        
    @staticmethod
    def get_address_book():
        addresses = StructureIO.get_employee_department_list()
        addresses.append("all")
        return addresses
    
    @staticmethod
    def exec_sql(sql: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()
            cursor.execute(sql)
            logs = cursor.fetchall()

            # カラム名を取得
            column_names = [desc[0] for desc in cursor.description]

            conn.commit()
            conn.close()

            return logs, column_names

        except Exception as e:
            print(f"DB SQL実行エラー: {e}")
            return None, None

class StructureIO:
    @staticmethod
    def create_structure_table():
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS structure(
                    id INTEGER PRIMARY KEY,
                    EmployeeName TEXT,
                    DepartmentName TEXT
                )
            """
            )

            conn.commit()
            conn.close()
            print("Structure table has been created.")
        except Exception as e:
            print(f"Structure table creation error: {e}")

    @staticmethod
    def insert_employee_departments(employee_name: str, department_names: list):
        for department in department_names:
            StructureIO.insert_employee_department(employee_name, department)

    @staticmethod
    def insert_employee_department(employee_name: str, department_name: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO structure (EmployeeName, DepartmentName) VALUES (?, ?)",
                (employee_name, department_name),
            )

            conn.commit()
            conn.close()
            print("Employee department information has been added.")
        except Exception as e:
            print(f"DB write error: {e}")

    @staticmethod
    def get_departments_of_employee(employee_name: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT DepartmentName FROM structure WHERE EmployeeName = ?", (employee_name,))
            departments = cursor.fetchall()

            conn.commit()
            conn.close()

            return [dept[0] for dept in departments]

        except Exception as e:
            print(f"DB read error: {e}")
            return []

    @staticmethod
    def get_employees_in_department(department_name: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT EmployeeName FROM structure WHERE DepartmentName = ?", (department_name,))
            employees = cursor.fetchall()

            conn.commit()
            conn.close()

            return [emp[0] for emp in employees]

        except Exception as e:
            print(f"DB read error: {e}")
            return []
        
    @staticmethod
    def get_employee_department_list():
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT DepartmentName, EmployeeName FROM structure")
            department_employee_pairs = cursor.fetchall()

            conn.commit()
            conn.close()

            department_employee_list = []
            for department, employee in department_employee_pairs:
                department_employee_list.append(department + "部")
                department_employee_list.append(employee)

            return list(set(department_employee_list))

        except Exception as e:
            print(f"DB読込エラー: {e}")
            return []

    @staticmethod
    def exec_sql(sql: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()

            # Get column names
            column_names = [desc[0] for desc in cursor.description]

            conn.commit()
            conn.close()

            return data, column_names

        except Exception as e:
            print(f"DB SQL execution error: {e}")
            return None, None

class DepartmentIO:
    @staticmethod
    def create_department_table():
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS department(
                    id INTEGER PRIMARY KEY,
                    Name TEXT,
                    Mission TEXT
                )
                """
            )

            conn.commit()
            conn.close()
            print("部門テーブルが作成されました。")
        except Exception as e:
            print(f"部門テーブル作成エラー: {e}")

    @staticmethod
    def add_department(name: str, mission: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO department (Name, Mission) VALUES (?, ?)",
                (name, mission),
            )

            conn.commit()
            conn.close()
            print("部門が追加されました。")
        except Exception as e:
            print(f"部門追加エラー: {e}")

    @staticmethod
    def get_mission_by_name(name: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT Mission FROM department WHERE Name=?", (name,))
            mission = cursor.fetchone()

            conn.close()

            if mission:
                return mission[0]
            else:
                print("指定された部門が見つかりませんでした。")
                return None

        except Exception as e:
            print(f"部門情報取得エラー: {e}")
            return None

    @staticmethod
    def get_all_departments():
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM department")
            departments = cursor.fetchall()

            # Get column names
            column_names = [desc[0] for desc in cursor.description]

            conn.close()

            if departments:
                department_dicts = [{"id":id, "name":name, "mission":mission} for id, name, mission in departments]
                return department_dicts,column_names
            else:
                print("部門情報がありません。")
                return [],[]

        except Exception as e:
            print(f"部門情報取得エラー: {e}")
            return [],[]

    @staticmethod
    def update_department(id: int, name: str, mission: str):
        try:
            conn = sqlite3.connect(common.DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE department SET Name = ?, Mission = ? WHERE ID = ?",
                (name, mission, id),
            )

            conn.commit()
            conn.close()
            print(f"部門 '{name}' の情報が更新されました。")
        except Exception as e:
            print(f"部門情報更新エラー: {e}")