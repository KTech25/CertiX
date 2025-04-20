import smtplib
from email.message import EmailMessage
import mimetypes
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def send_certificate(student_email, student_name, certificate_path):

    """
    Sends the certificate to the provided student's email address.

    :param student_email: Email address of the student
    :param student_name: Name of the student
    :param certificate_path: Path to the certificate image file
    """


    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("PASSWORD")
    
    # Configuration
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    subject = "Your Certificate"
    body = f"Dear {student_name},\n\nCongratulations on Completing the Workshop! Please find your certificate attached.\n\nBest regards,\nTeam GDGOC-SVVV"

    # Create Email
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = student_email
    msg.set_content(body)

    # Attach the certificate image
    mime_type, _ = mimetypes.guess_type(certificate_path)
    mime_main, mime_sub = mime_type.split('/')

    with open(certificate_path, "rb") as cert_file:
        msg.add_attachment(cert_file.read(),
                           maintype=mime_main,
                           subtype=mime_sub,
                           filename=certificate_path.split("/")[-1])

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            print(f"✔️ Certificate sent to {student_name} ({student_email})")
    except Exception as e:
        print(f"❌ Failed to send email to {student_name} ({student_email}): {e}")
        # If email fails, append the student's info to the file
        failed_student = f"{student_name} <{student_email}>"
        
        # Check if the failed_emails.txt file exists, if not create it and append the failed email
        file_path = "failed_emails.txt"
        with open(file_path, "a") as file:
            file.write(failed_student + "\n")

    # File is automatically closed after using 'with open', so no need to explicitly close it
