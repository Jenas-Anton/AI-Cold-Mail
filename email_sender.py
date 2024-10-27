# email_sender.py

import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import Dict, Tuple, Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.credentials: Optional[Dict[str, str]] = None
        
    def verify_credentials(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Verify Gmail credentials by attempting to establish a connection
        
        Returns:
            Tuple[bool, str]: (success status, message)
        """
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.set_debuglevel(1)
            server.starttls()
            server.login(email, password)
            server.quit()
            
            self.credentials = {"email": email, "password": password}
            logger.info("Gmail credentials verified successfully")
            return True, "Credentials verified successfully"
            
        except Exception as e:
            logger.error(f"Credential verification failed: {str(e)}")
            return False, str(e)
    
    def send_test_email(self, recipient: str) -> Tuple[bool, str]:
        """
        Send a test email to verify the setup
        
        Returns:
            Tuple[bool, str]: (success status, message)
        """
        if not self.credentials:
            return False, "Credentials not set. Please verify credentials first."
            
        subject = "Test Email From Job Application Assistant"
        body = "This is a test email to verify the email sending functionality works."
        
        return self.send_email(recipient, subject, body)
    
    def send_email(self, recipient: str, subject: str, body: str) -> Tuple[bool, str]:
        """
        Send an email using the verified Gmail credentials
        
        Returns:
            Tuple[bool, str]: (success status, message)
        """
        if not self.credentials:
            return False, "Credentials not set. Please verify credentials first."
            
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.credentials["email"]
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Establish connection
            logger.info("Connecting to SMTP server...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.set_debuglevel(1)
            
            logger.info("Starting TLS...")
            server.starttls()
            
            logger.info("Logging in...")
            server.login(self.credentials["email"], self.credentials["password"])
            
            # Send email
            logger.info("Sending email...")
            text = msg.as_string()
            server.sendmail(self.credentials["email"], recipient, text)
            
            logger.info("Closing connection...")
            server.quit()
            
            return True, "Email sent successfully!"
            
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
            
    def send_bulk_emails(self, recipients: list, subject: str, body: str) -> Dict[str, bool]:
        """
        Send the same email to multiple recipients
        
        Returns:
            Dict[str, bool]: Dictionary mapping recipient emails to success status
        """
        results = {}
        for recipient in recipients:
            success, _ = self.send_email(recipient, subject, body)
            results[recipient] = success
        return results