import os
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'mera_secret_key'  # जरूरी होता है session के लिए

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
            return redirect(url_for('dashboard'))  # <-- Fixed: redirect to 'dashboard'
        else:
            return render_template('login.html', error="गलत पासवर्ड")
    return render_template('login.html')

@app.before_request
def protect_dashboard():
    if request.endpoint not in ['login', 'static', 'verify', 'trade'] and not session.get('logged_in'):
        return redirect(url_for('login'))

@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

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

@app.route('/verify')
def verify():
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
            return jsonify({'status': 'Message sent to Telegram successfully!'}), 200
        else:
            return jsonify({'status': 'Failed to send message', 'error': response.text}), 500
    return jsonify({'status': 'No message provided'}), 400

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)




