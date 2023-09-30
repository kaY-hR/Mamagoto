import os

@staticmethod
def print_directory_structure(directory, indent=0):
    result = ""
    # ディレクトリ内のファイルとサブディレクトリを取得
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir():
                # サブディレクトリの場合は再帰的に表示
                result += "  " * indent + "|--" + entry.name +"\n"
                result += print_directory_structure(entry.path, indent + 1)
            elif entry.is_file():
                # ファイルの場合はそのまま表示
                result += "  " * indent + "|--" + entry.name +"\n"
        return result
