import smtplib
from email.message import EmailMessage
import mimetypes
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from the .env file
load_dotenv()


def send_certificate(student_email, student_name, certificate_path):
    """
    Sends the certificate (converted to PDF) to the provided student's email address.

    :param student_email: Email address of the student
    :param student_name: Name of the student
    :param certificate_path: Path to the certificate image file (.png)
    """

    sender_email = "gdscsvvv@gmail.com"
    sender_password = "rqvw tbap obvt brki"
    subject = "GDGOC-SVVV Web Dev Workshop Certificate"
    body = f"""Dear {student_name},

Congratulations on successfully completing the Web Development Workshop organized by GDGOC-SVVV!

We hope the sessions were insightful and gave you a solid foundation to continue your journey in web development. As a token of appreciation for your participation and dedication, we are pleased to share your certificate of completion, attached with this email.

If you have any questions, need further guidance, or would like to stay updated on upcoming tech events, feel free to reach out to us or follow our official pages.

Wishing you all the best in your future endeavors!

Warm regards,  
Team GDGOC-SVVV
"""

    # Convert PNG to PDF
    certificate_pdf_path = certificate_path.replace(".png", ".pdf")
    try:
        image = Image.open(certificate_path)
        rgb_image = image.convert("RGB")
        rgb_image.save(certificate_pdf_path)
    except Exception as e:
        print(f"❌ Failed to convert certificate for {student_name}: {e}")
        return

    # Create Email
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = student_email
    msg.set_content(body)

    # Attach the certificate PDF
    with open(certificate_pdf_path, "rb") as cert_file:
        msg.add_attachment(cert_file.read(),
                           maintype="application",
                           subtype="pdf",
                           filename=os.path.basename(certificate_pdf_path))

    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
            print(f"✔️ Certificate sent to {student_name} ({student_email})")
    except Exception as e:
        print(f"❌ Failed to send email to {student_name} ({student_email}): {e}")
        failed_student = f"{student_name} <{student_email}>"
        with open("failed_emails.txt", "a") as file:
            file.write(failed_student + "\n")
    finally:
        # Optional: Clean up the generated PDF file
        if os.path.exists(certificate_pdf_path):
            os.remove(certificate_pdf_path)
