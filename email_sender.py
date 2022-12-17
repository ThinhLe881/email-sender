import smtplib
import ssl
from email.message import EmailMessage
import mimetypes
import creds
import content
import glob


def main():
    sender_email = creds.sender
    recipient_email = creds.recipient
    password = creds.password

    print("Sender: " + sender_email)
    print("Recipient: " + str(recipient_email))

    body = content.body
    subject = content.subject

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.add_alternative(body, subtype="html")

    images = content.images
    # embed images (for html content, otherwise put in 'attachments/')
    embedded_images_count = 0
    for image in glob.glob('images/*.*'):
        embedded_images_count += 1
        file_name = image.split('\\')[1]
        with open(image, 'rb') as img:
            maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')
            message.get_payload()[0].add_related(
                img.read(), maintype=maintype, subtype=subtype, cid=images[file_name])

    # add attachments
    attachments_count = 0
    for file in glob.glob('attachments/*.*'):
        attachments_count += 1
        with open(file, 'rb') as f:
            file_name = f.name.split('\\')[1]
            maintype, subtype = mimetypes.guess_type(file_name)[0].split('/')
            message.add_attachment(
                f.read(), maintype=maintype, subtype=subtype, filename=file_name)

    context = ssl.create_default_context()

    print("Attachments: " + str(attachments_count) +
        " | Embedded Images: " + str(embedded_images_count))
    print("Sending email...")

    # for Gmail, account needs 2-steps verification and app password generated
    smtp_server = "smtp.gmail.com"

    # for Outlook
    # smtp_server = "smtp.office365.com"

    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())

    print("Email sent")

if __name__ == "__main__":
    main()
