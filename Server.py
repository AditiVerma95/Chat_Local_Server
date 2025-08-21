from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@socketio.on("message")
def handle_message(msg):
    # Pass through unchanged; clients decide what to show
    emit("message", msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
