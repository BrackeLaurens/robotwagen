from flask import Flask, render_template, Response
import socket
import threading
import json

app = Flask(__name__)

# Global variable to store the latest data
latest_data = {"value": "No data received yet"}

def udp_listener():
    UDP_IP = "0.0.0.0"  # Listen on all available interfaces
    UDP_PORT = 5005     # Choose a port number

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        global latest_data
        try:
            latest_data = {"value": data.decode('utf-8')}
        except:
            latest_data = {"value": "Error decoding data"}

# Start UDP listener in a background thread
listener_thread = threading.Thread(target=udp_listener)
listener_thread.daemon = True
listener_thread.start()

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app 