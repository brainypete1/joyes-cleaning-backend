from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_mail import Mail, Message
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # allow frontend to call API

# --- Gmail SMTP config via environment variables ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("joyescleaningservices@gmail.com")  # secure
app.config['MAIL_PASSWORD'] = os.environ.get("tskf htvl imqt mljd")  # secure

mail = Mail(app)

# --- Serve frontend ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Health check route ---
@app.route("/health")
def health():
    return jsonify({"status": "running", "service": "Joyes Cleaning Backend"})

# --- API endpoint to send quote ---
@app.route('/api/send-quote', methods=['POST'])
def send_quote():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    service = data.get('service')
    message = data.get('message')

    try:
        msg = Message(
            subject=f"New Cleaning Request from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"""
Name: {name}
Email: {email}
Phone: {phone}
Service: {service}
Message: {message}
"""
        )
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'message': str(e)}), 500

# --- Run ---
if __name__ == '__main__':
    app.run(debug=True)
