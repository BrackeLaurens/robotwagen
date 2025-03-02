from app import app
from flask import render_template, Response
from app import latest_data
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            # Send data every second
            yield f"data: {json.dumps(latest_data)}\n\n"
            import time
            time.sleep(1)
    
    return Response(event_stream(), mimetype="text/event-stream") 