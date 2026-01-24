# joyes-cleaning-backend[Uploading app.py…]()
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "Joyes Cleaning Backend"
    })

# --- Configure Gmail SMTP ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'joyescleaningservices@gmail.com'
app.config['MAIL_PASSWORD'] = 'tskf htvl imqt mljd'

mail = Mail(app)

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

if __name__ == '__main__':
    app.run()[requirements.txt](https://github.com/user-attachments/files/24835942/requirements.txt)

flask
flask-cors
flask-mail
gunicorn
