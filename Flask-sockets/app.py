from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
#inicializar la conexion de webSockets
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

#Configuracion para la escucha de eventos
@socketio.on('message')
def handleMessage(message):
    print('Message: ', message)
    send(message, broadcast = True)



if __name__ == "__main__":
    socketio.run(app, host='192.168.1.68')