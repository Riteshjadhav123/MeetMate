import smtplib
import os
import sys
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def send_summary_email(sender=None, recipient=None):
    """
    Emails the meeting summary to a specified recipient from a specified sender.
    """
    load_dotenv()
    sender = sender or os.getenv("SENDER_EMAIL")
    recipient = recipient or os.getenv("RECIPIENT_EMAIL")
    password = (os.getenv("GMAIL_APP_PASSWORD") or "").replace(" ", "").strip()
    
    if not sender or not recipient:
        print("Error: SENDER_EMAIL or RECIPIENT_EMAIL not found in environment variables.")
        return

    if not password:
        print("Error: GMAIL_APP_PASSWORD not found in .env file.")
        return

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = "✅ Meeting Summary from MeetMate"
    body = "Hi team,\n\nPlease find the summary attached.\n\nBest,\nMeetMate Bot"
    msg.attach(MIMEText(body, 'plain'))

    # Attach the summary file
    summary_filepath = 'outputs/meeting_summary.txt'
    try:
        with open(summary_filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=meeting_summary.txt')
        msg.attach(part)
    except FileNotFoundError:
        print(f"Error: The file '{summary_filepath}' was not found.")
        return

    # Connect to the server and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            print(f"✅ Email sent successfully to {recipient}!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    send_summary_email()