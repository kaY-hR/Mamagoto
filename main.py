import threading
from run_server import run_server
from run_mamagoto import run_mamagoto

if __name__ == "__main__":

    # スレッドを作成して実行
    thread_server = threading.Thread(target=run_server)
    thread_main = threading.Thread(target=run_mamagoto)

    # スレッドを開始
    thread_server.start()
    thread_main.start()

    thread_server.join()
    thread_main.join()
