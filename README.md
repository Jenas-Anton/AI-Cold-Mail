# 🤖 AI-Cold-Mail

An intelligent Streamlit application that revolutionizes your cold emailing process with AI-powered personalized email generation. Perfect for job applications, business development, and networking!

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🧠 AI-powered personalized email generation using Groq AI
- 📄 Resume/document parsing (PDF and DOCX support)
- 📧 Seamless Gmail integration
- 🎯 Smart context analysis for personalization
- ✉️ Bulk email capabilities
- 🧪 Test email functionality
- 🔐 Secure credential handling
- ⚡ Real-time email preview

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-cold-mail.git
cd ai-cold-mail
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:
```
streamlit
groq
python-docx
PyPDF2
python-dotenv
```

## 🔑 Configuration

1. Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
```

2. Gmail Setup (Required for sending emails):
- Enable 2-Factor Authentication in your Google Account
- Generate an App Password: 
  1. Go to Google Account Settings
  2. Security
  3. 2-Step Verification
  4. App Passwords
  5. Generate a new app password for "Mail"

## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the web interface (default: `http://localhost:8501`)

### 📝 Setup Tab

1. **Document Upload**
   - Upload your resume/document (PDF or DOCX)
   - Review extracted text
   - Make sure all relevant information is captured

2. **Gmail Configuration**
   - Enter your Gmail address
   - Input your App Password
   - Verify connection with test email

### ✉️ Compose & Send Tab

1. **Recipient Management**
   - Add multiple recipient emails
   - Send test emails to verify addresses
   - Easily remove recipients

2. **Content Generation**
   - Input job description or cold email context
   - AI analyzes and generates personalized emails
   - Preview before sending
   - Bulk send to all recipients

## 💡 Advanced Features

### Email Personalization
The AI analyzes your input and recipient context to create highly personalized emails that:
- Match your profile to the recipient's needs
- Include relevant keywords and phrases
- Maintain a professional yet engaging tone
- Create compelling subject lines
- End with clear calls to action

### Bulk Sending
- Send personalized emails to multiple recipients
- Track sending status for each recipient
- Error handling and retry capabilities
- Success/failure notifications

## 🔒 Security Notes

- Store sensitive keys in `.env` file (never commit to repo)
- Use Gmail App Passwords instead of account passwords
- Regularly rotate API keys and credentials
- Session-only credential storage
- No permanent data storage

## 🏗️ Project Structure

```
ai-cold-mail/
├── app.py                 # Streamlit interface
├── email_code.py         # Email generation logic
├── requirements.txt      # Dependencies
├── .env                 # Configuration (not in repo)
└── README.md            # Documentation
```

## ⚙️ Core Components

- `EmailGenerator`: Manages email generation and sending
- `initialize_session_state()`: Handles Streamlit session
- `read_resume()`: Document parsing
- `verify_gmail()`: Email credential verification
- `generate_and_send_email()`: Core email functionality

## ⚠️ Limitations

- Gmail-only email sending support
- Document parsing accuracy varies
- API rate limits apply
- Internet connection required
- Streamlit session limitations

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -am 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Web framework
- [Groq](https://groq.com/) - AI capabilities
- [Python-DOCX](https://python-docx.readthedocs.io/) - DOCX parsing
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF parsing

## 📞 Support

For support:
- Open an issue in the GitHub repository
- Contact project maintainers
- Check existing documentation

## 🎯 Future Enhancements

- Support for additional email providers
- Advanced template customization
- Analytics dashboard
- Integration with CRM systems
- Mail merge capabilities
- Scheduling functionality

---

