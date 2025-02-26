import smtplib

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'prasadyammi2@gmail.com'
EMAIL_PASSWORD = 'jgkd udby yfrb dwbv'  # Use your app password

def send_test_email():
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            message = 'Subject: Test Email\n\nThis is a test email.'
            server.sendmail(EMAIL_ADDRESS, 'ppkkhar2020@gmail.com', message)
        print('Test email sent successfully')
    except Exception as e:
        print(f'Error sending test email: {str(e)}')

if __name__ == '__main__':
    send_test_email()