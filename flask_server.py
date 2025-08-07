from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)
signals = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_signals")
def get_signals():
    return jsonify(signals)

@app.route("/get-signal")
def get_signal():
    return jsonify({"message": "Signal fetched successfully!"})

@app.route('/api/trade', methods=['POST'])
def trade():
    data = request.get_json()
    symbol = data.get('symbol')
    signal_type = data.get('signal')
    amount = data.get('amount')

    if signal_type and signal_type.lower() == "buy":
        signal_type = "call"
    elif signal_type and signal_type.lower() == "sell":
        signal_type = "put"

    signals[symbol] = {
        'signal': signal_type,
        'amount': amount,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
