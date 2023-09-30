import threading
import webbrowser
from WebUIServer.flaskserver import FlaskServer

def run_server():
    flask_thread = threading.Thread(target = lambda:FlaskServer.app.run(debug=False, host="127.0.0.1", port=5000))
    flask_thread.start()
    webbrowser.open("http://127.0.0.1:5000")
    flask_thread.join()

if __name__ == "__main__":
    run_server()