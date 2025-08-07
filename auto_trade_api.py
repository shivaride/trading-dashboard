from flask import Flask, jsonify, request
from datetime import datetime

# Configure the Flask application
app = Flask(__name__)

signals = {}

@app.route('/api/trade', methods=['POST'])
def trade():
    """
    An API endpoint to receive trading signals from a JSON payload.
    """
    # Ensure the incoming data is in JSON format
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    try:
        data = request.get_json()

        # Get the necessary information from the JSON data
        symbol = data.get('symbol')
        direction = data.get('signal')  # "call" (UP) or "put" (DOWN)
        amount = data.get('amount', 10)  # Default amount is 10 if not provided

        # Ensure 'symbol' and 'signal' are present
        if not all([symbol, direction]):
            return jsonify({"status": "error", "message": "Missing 'symbol' or 'signal' in JSON payload"}), 400

        signals[symbol] = {
            'signal': direction,
            'amount': amount,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return jsonify({"status": "success", "message": "Trade signal received and logged"}), 200

    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({"status": "error", "message": "An internal server error occurred"}), 500

@app.route('/get_signals', methods=['GET'])
def get_signals():
    """
    An API endpoint to retrieve the latest trading signals.
    """
    return jsonify(signals)

if __name__ == '__main__':
    # In debug mode, the server will automatically reload on any code changes
    app.run(host='0.0.0.0', port=5001, debug=True)