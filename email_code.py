import logging
from groq import Groq
import PyPDF2
from docx import Document
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmailGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"
        self.gmail_creds = None
        
    def read_resume(self, uploaded_file):
        """Extract text from the uploaded resume file (PDF or DOCX)"""
        try:
            file_type = uploaded_file.type if hasattr(uploaded_file, 'type') else uploaded_file.name.split('.')[-1]
            
            if file_type == "application/pdf" or file_type.lower() == 'pdf':
                reader = PyPDF2.PdfReader(uploaded_file)
                resume_text = ''
                for page in reader.pages:
                    resume_text += page.extract_text()
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file_type.lower() == 'docx':
                doc = Document(uploaded_file)
                resume_text = '\n'.join([para.text for para in doc.paragraphs])
            else:
                return None, "Unsupported file format. Please upload a PDF or DOCX file."

            if not resume_text.strip():
                return None, "No text could be extracted from the file."

            return resume_text.strip(), None
        except Exception as e:
            logger.error(f"Error reading resume: {str(e)}")
            return None, f"Error reading the resume: {str(e)}"

    def verify_gmail(self, email, password):
        """Verify Gmail credentials"""
        try:
            logger.info("Attempting to connect to SMTP server...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(1)
            
            logger.info("Starting TLS...")
            server.starttls()
            
            logger.info("Attempting login...")
            server.login(email, password)
            
            logger.info("Closing server connection...")
            server.quit()
            
            self.gmail_creds = {"email": email, "password": password}
            return True
            
        except Exception as e:
            logger.error(f"Gmail verification failed: {str(e)}")
            return False

    def send_test_email(self, recipient):
        """Send test email to a specified recipient"""
        if not self.gmail_creds:
            return False, "Gmail credentials not set"
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_creds["email"]
            msg['To'] = recipient
            msg['Subject'] = "Test Email From Job Application Assistant"
            
            body = "This is a test email to verify the email sending functionality works."
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(1)
            server.starttls()
            server.login(self.gmail_creds["email"], self.gmail_creds["password"])
            
            text = msg.as_string()
            server.sendmail(self.gmail_creds["email"], recipient, text)
            server.quit()
            
            return True, "Test email sent successfully!"
            
        except Exception as e:
            logger.error(f"Error sending test email: {str(e)}")
            return False, str(e)

    def generate_and_send_email(self, job_description, user_profile, recipient, gmail_creds):
        """Generate and send email in one step"""
        if not user_profile:
            logger.error("User profile/resume is missing")
            return False, "Missing user profile/resume"

        if not gmail_creds:
            logger.error("Gmail credentials not set")
            return False, "Gmail credentials not set"

        prompt = f"""You are an expert email writer for job applications. Generate a compelling email for the following job:

Job Description: {job_description}

Candidate Profile:
{user_profile}

Generate a professional email that:
1. Has a compelling subject line
2. Opens with a strong hook (avoid generic openings)
3. Shows specific interest in the company/role
4. Matches candidate's experience to job requirements
5. Has a confident but humble tone
6. Ends with a clear call to action
7. Keeps paragraphs concise and well-structured
8. Includes relevant keywords from the job description
9. Keep it under 250 words 
10. Mention all the social links at the end after the best regards

Format response exactly as:
SUBJECT: [Your subject line]

[Your email body]

---END---"""

        try:
            # Generate email content
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=1000
            )

            content = response.choices[0].message.content
            parts = content.split("SUBJECT:", 1)
            
            if len(parts) <= 1:
                return False, "Failed to generate email content"

            email_content = parts[1].split("---END---")[0].strip()
            subject_and_body = email_content.split("\n", 1)
            
            if len(subject_and_body) != 2:
                return False, "Failed to parse email content"

            subject = subject_and_body[0].strip()
            body = subject_and_body[1].strip()

            # Send email
            try:
                msg = MIMEMultipart()
                msg['From'] = gmail_creds["email"]
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                logger.info("Connecting to SMTP server...")
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.set_debuglevel(1)
                
                server.starttls()
                server.login(gmail_creds["email"], gmail_creds["password"])
                
                logger.info("Sending email...")
                text = msg.as_string()
                server.sendmail(gmail_creds["email"], recipient, text)
                
                server.quit()
                logger.info("Email sent successfully!")
                
                return True, {
                    "subject": subject,
                    "body": body,
                    "status": "Email sent successfully!"
                }

            except Exception as e:
                logger.error(f"Error sending email: {str(e)}")
                return False, f"Failed to send email: {str(e)}"

        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            return False, f"Failed to generate email: {str(e)}"