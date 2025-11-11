from flask import Flask, jsonify
from datetime import datetime 
from pytz import timezone

app = Flask(__name__)

@app.route('/time', methods=['GET'])
def get_current_time_date():
    """Endpoint to get the current server time and date."""
    current_time =datetime.now()
    current_date = current_time.strftime("%Y-%m-%d")
    current_time = current_time.strftime("%H:%M:%S")
    return jsonify({'current_date':current_date},{'current_time': current_time})


if __name__ == '__main__': # Run the Flask app on host
    app.run(host='0.0.0.0', port=8080) # Listen on all interfaces at port 8080