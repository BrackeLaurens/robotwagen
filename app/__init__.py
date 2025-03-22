from flask import Flask, render_template, Response, redirect, url_for, flash
import socket
import threading
import json
import os

# Move latest_data declaration
latest_data = {"value": "No data received yet"}

def udp_listener():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Add both these socket options
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.settimeout(1)
        print(f"Attempting to bind to port {UDP_PORT}...")
        sock.bind((UDP_IP, UDP_PORT))
        print(f"Successfully bound to port {UDP_PORT}")

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print(f"Received data from {addr}")
                global latest_data
                try:
                    latest_data = {"value": data.decode('utf-8')}
                except:
                    latest_data = {"value": "Error decoding data"}
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error receiving data: {e}")

    except Exception as e:
        print(f"Failed to create/bind socket: {e}")
        return

def create_app():
    app = Flask(__name__)
    app.debug = False  # Disable debug mode, or
    
    # Only start the UDP listener in the main process
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        if not any(thread.name == 'udp_listener' for thread in threading.enumerate()):
            listener_thread = threading.Thread(target=udp_listener, name='udp_listener')
            listener_thread.daemon = True
            listener_thread.start()
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app 