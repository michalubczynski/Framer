from adafruit_mlx90640 import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep

import busio
import board

i2c = busio.I2C(board.SCL,board.SDA)

sensor = MLX90640(i2c)

sensor.refresh_rate = RefreshRate.REFRESH_2_HZ

time.sleep(1)

tabFrame = [None] * 768


app = Flask('SERWIS')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('collect')
def my_event(message):
	while True:
		sensor.getFrame(tabFrame)
		print('SPAM')
		emit('frame', {'frameData': tabFrame})
		sleep(0.5)
		
if __name__ == '__main__':
    socketio.run(app)

print(tabFrame)
