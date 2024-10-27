from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_gmail_connection(sender_email, app_password, recipient_email):
    """
    Simple test function to verify Gmail connection and send a test email
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Test Email From Python"
        
        body = "This is a test email to verify the SMTP connection works."
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        logger.info("Attempting to connect to SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1)  # Enable debug output
        
        logger.info("Starting TLS...")
        server.starttls()
        
        logger.info("Attempting login...")
        server.login(sender_email, app_password)
        
        logger.info("Sending email...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        
        logger.info("Closing server connection...")
        server.quit()
        
        return True, "Email sent successfully!"
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False, str(e)

# Save this as test_email.py and run it:
if __name__ == "__main__":
    sender_email = input("Enter your Gmail address: ")
    app_password = input("Enter your App Password: ")
    recipient_email = input("Enter recipient email: ")
    
    success, message = test_gmail_connection(sender_email, app_password, recipient_email)
    print(f"\nResult: {'Success' if success else 'Failed'}")
    print(f"Message: {message}")