from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)  


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'marierareagan@gmail.com'  
SMTP_PASSWORD = 'ppwkysfmuntbeayn' 
EMAIL_FROM = 'marierareagan@gmail.com'  
EMAIL_TO = 'marierareagan@gmail.com'  

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'All fields are required.'}), 400

    # Email to you (the recipient)
    subject_to_you = 'New Contact Form Submission'
    body_to_you = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg_to_you = MIMEMultipart()
    msg_to_you['From'] = EMAIL_FROM
    msg_to_you['To'] = EMAIL_TO
    msg_to_you['Subject'] = subject_to_you
    msg_to_you.attach(MIMEText(body_to_you, 'plain'))

   
    subject_to_user = 'Thank you for contacting us!'
    body_to_user = f"Dear {name},\n\nThank you for reaching out to me. i have received your message and will get back to you shortly.\n\nBest regards,\nENG. Reagan"

    msg_to_user = MIMEMultipart()
    msg_to_user['From'] = EMAIL_FROM
    msg_to_user['To'] = email  
    msg_to_user['Subject'] = subject_to_user
    msg_to_user.attach(MIMEText(body_to_user, 'plain'))

    try:
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg_to_you.as_string())
            
            
            server.sendmail(EMAIL_FROM, email, msg_to_user.as_string())

        return jsonify({'success': 'Message sent successfully!'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to send message. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
