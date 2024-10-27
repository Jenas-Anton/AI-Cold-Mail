import streamlit as st
from email_code import EmailGenerator

def initialize_session_state():
    """Initialize all session state variables"""
    if 'generator' not in st.session_state:
        api_key = st.secrets["GROQ_API_KEY"]
        st.session_state.generator = EmailGenerator(api_key)
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
    if 'recipients' not in st.session_state:
        st.session_state.recipients = []
    if 'gmail_verified' not in st.session_state:
        st.session_state.gmail_verified = False
    if 'gmail_creds' not in st.session_state:
        st.session_state.gmail_creds = None

def add_recipient():
    """Add a new recipient email to the list"""
    new_recipient = st.session_state.new_recipient.strip()
    if new_recipient and new_recipient not in st.session_state.recipients:
        st.session_state.recipients.append(new_recipient)
    st.session_state.new_recipient = ""

def remove_recipient(email):
    """Remove a recipient email from the list"""
    st.session_state.recipients.remove(email)

def send_test_email_for_recipient(email):
    """Send a test email to a specific recipient"""
    if st.session_state.generator and st.session_state.gmail_creds:
        success, message = st.session_state.generator.send_test_email(email)
        if success:
            st.success(f"Test email sent successfully to {email}")
        else:
            st.error(f"Failed to send test email to {email}: {message}")

def main():
    st.title("AI Job Application Assistant")
    st.markdown("""🤖 Your personal AI assistant for crafting and sending job applications""")

    initialize_session_state()

    setup_tab, compose_tab = st.tabs(["📝 Setup", "✉️ Compose & Send"])

    # Setup Tab
    with setup_tab:
        col1, col2 = st.columns(2)

        # Resume Upload Section
        with col1:
            st.header("Upload Resume")
            uploaded_file = st.file_uploader("Choose your resume file", type=['pdf', 'docx'])

            if uploaded_file:
                with st.spinner("Processing resume..."):
                    resume_text, error = st.session_state.generator.read_resume(uploaded_file)

                    if error:
                        st.error(error)
                    else:
                        st.session_state.resume_text = resume_text
                        st.success("Resume processed successfully!")
                        with st.expander("View extracted text"):
                            st.text(resume_text)

        # Gmail Setup Section
        with col2:
            st.header("Gmail Setup")
            sender_email = st.text_input("Your Gmail Address")
            app_password = st.text_input("App Password", type="password")

            if st.button("Verify Gmail"):
                if sender_email and app_password:
                    with st.spinner("Verifying Gmail access..."):
                        if st.session_state.generator.verify_gmail(sender_email, app_password):
                            st.session_state.gmail_verified = True
                            st.session_state.gmail_creds = {"email": sender_email, "password": app_password}
                            st.success("Gmail credentials verified successfully!")
                        else:
                            st.error("Gmail verification failed. Please check your credentials.")
                else:
                    st.warning("Please enter both email and app password")

    # Compose & Send Tab
    with compose_tab:
        # Check prerequisites
        if not st.session_state.resume_text:
            st.warning("Please upload your resume in the Setup tab first.")
            return
        if not st.session_state.gmail_verified:
            st.warning("Please verify your Gmail credentials in the Setup tab first.")
            return

        # Recipients Section
        st.header("Recipients")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("Add recipient email", key="new_recipient", placeholder="Enter email address and click Add")
        with col2:
            st.button("Add", on_click=add_recipient)

        # Display recipients with Send Test Email button
        if st.session_state.recipients:
            st.write("Current recipients:")
            for email in st.session_state.recipients:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.text(email)
                with col2:
                    st.button("Remove", key=f"remove_{email}", on_click=remove_recipient, args=(email,))
                with col3:
                    if st.button("Send Test Email", key=f"test_{email}"):
                        send_test_email_for_recipient(email)
        else:
            st.info("No recipients added yet.")

        # AI Chat Section
        st.header("Job Description Chat")
        st.info("Describe the job position or paste the job description. The AI will help craft a personalized email.")

        # Chat input
        user_input = st.text_area("Describe the job or ask questions", placeholder="Paste job description or ask questions about crafting the email...")

        if st.button("Generate and Send Email"):
            if not user_input:
                st.warning("Please enter a job description or question.")
                return

            if not st.session_state.recipients:
                st.error("Please add at least one recipient before sending.")
                return

            # Generate and send email to each recipient
            with st.spinner("Generating and sending emails..."):
                success_count = 0
                for recipient in st.session_state.recipients:
                    success, result = st.session_state.generator.generate_and_send_email(
                        user_input,
                        st.session_state.resume_text,
                        recipient,
                        st.session_state.gmail_creds
                    )
                    
                    if success:
                        success_count += 1
                        st.success(f"Email sent successfully to {recipient}")
                        
                        # Display the sent email content
                        with st.expander(f"View email sent to {recipient}"):
                            st.text_input("Subject", value=result["subject"], disabled=True)
                            st.text_area("Body", value=result["body"], height=300, disabled=True)
                    else:
                        st.error(f"Failed to send email to {recipient}: {result}")

                # Final summary
                if success_count == len(st.session_state.recipients):
                    st.success("All emails sent successfully!")
                elif success_count == 0:
                    st.error("Failed to send any emails.")
                else:
                    st.warning(f"Successfully sent {success_count} out of {len(st.session_state.recipients)} emails.")

if __name__ == "__main__":
    main()