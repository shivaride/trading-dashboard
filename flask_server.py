import os
import logging  # <-- Add this import
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from datetime import datetime
import requests
from flask_socketio import SocketIO, emit
from flask_cors import CORS  # <-- Add this import

# Set up logging
logging.basicConfig(level=logging.INFO)  # <-- Add this line

app = Flask(__name__)
CORS(app)  # <-- Add this line to enable CORS

app.secret_key = 'mera_secret_key'  # जरूरी होता है session के लिए

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# 🔐 Set your password here
DASHBOARD_PASSWORD = 'MeraDashboard@2025'

signals = {}

TELEGRAM_BOT_TOKEN = '8452064311:AAGzJo8-JqpddDqiy7mzB4_Pz9t5xCJ1FmU'
TELEGRAM_CHAT_ID = '8240596669'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == DASHBOARD_PASSWORD:
            session['logged_in'] = True
            logging.info("User logged in successfully.")  # <-- Add logging
            return redirect(url_for('dashboard'))  # <-- Fixed: redirect to 'dashboard'
        else:
            logging.warning("Login attempt with wrong password.")  # <-- Add logging
            return render_template('login.html', error="गलत पासवर्ड")
    return render_template('login.html')

@app.before_request
def protect_dashboard():
    if request.endpoint not in ['login', 'static', 'verify', 'trade'] and not session.get('logged_in'):
        logging.info(f"Unauthorized access attempt to {request.endpoint}.")  # <-- Add logging
        return redirect(url_for('login'))

@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        logging.info("Dashboard access without login, redirecting.")  # <-- Add logging
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route("/get_signal")
def get_signal():
    logging.info("Signals requested.")  # <-- Add logging
    return jsonify(signals)

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

    app.logger.info(f"Received signal: {symbol} - {signal_type}")  # <-- Added line

    signals[symbol] = {
        'signal': signal_type,
        'amount': amount,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    logging.info(f"Trade signal received: {signals[symbol]}")  # <-- Add logging

    return jsonify({"status": "received"}), 200

@app.route('/verify')
def verify():
    logging.info("Health check endpoint called.")  # <-- Add logging
    return jsonify({"message": "App working perfectly on Render!"})

@app.route('/send_telegram', methods=['POST'])
def send_telegram():
    data = request.get_json()
    message = data.get('message', '')

    if message:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message
        }
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            logging.info("Message sent to Telegram successfully.")  # <-- Add logging
            return jsonify({'status': 'Message sent to Telegram successfully!'}), 200
        else:
            logging.error(f"Failed to send message to Telegram: {response.text}")  # <-- Add logging
            return jsonify({'status': 'Failed to send message', 'error': response.text}), 500
    logging.warning("No message provided for Telegram.")  # <-- Add logging
    return jsonify({'status': 'No message provided'}), 400

@app.route('/api/send_signal', methods=['POST'])
def send_signal():
    data = request.get_json()
    symbol = data.get('symbol', 'EUR/USD')
    signal = data.get('signal', 'call')
    time = data.get('time', '1 MIN')

    socketio.emit('new_signal_event', {
        'symbol': symbol,
        'signal': signal,
        'time': time
    })
    logging.info(f"Signal sent via socket: {symbol}, {signal}, {time}")  # <-- Add logging
    return jsonify({"status": "Signal sent"}), 200

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    logging.info("User logged out.")  # <-- Add logging
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Use 'allow_unsafe_werkzeug=True' for Flask-SocketIO in development with Werkzeug
    logging.info(f"Starting server on port {port}...")  # <-- Add logging
    socketio.run(app, host="0.0.0.0", port=port, debug=True, allow_unsafe_werkzeug=True)






