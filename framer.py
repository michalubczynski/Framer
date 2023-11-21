from adafruit_mlx90640 import *
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep

import busio
import board

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

sensor = MLX90640(i2c)

sensor.refresh_rate = RefreshRate.REFRESH_2_HZ

tabFrame = [0.] * 768


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
def my_event():
	while True:
		sensor.getFrame(tabFrame)
		filteredFrame = [round(x, 3) for x in tabFrame]
		filteredFrame[704] = filteredFrame[705]
		emit('frame', {'frameData': filteredFrame})
		socketio.sleep(0.5)

		
if __name__ == '__main__':
    

	socketio.run(app, host="0.0.0.0")
	print('Killing Sever!!!')
