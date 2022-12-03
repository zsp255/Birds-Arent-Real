import smtplib  # Built in python modules 
import ssl
from email.mime.application import MIMEApplication  # Built in python modules 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Reference

### 2FA device password: pfsakavhmoalgkbrs

ctx = ssl.create_default_context()
password = "pfsakavhmoalgkbr"    # Your app password goes here
sender = "realbirdproject@gmail.com"    # Your e-mail address
receiver = "angelzouyifan@gmail.com" # Recipient's address

### Create the message
message = MIMEMultipart("mixed")
message["Subject"] = "Hello Mixed Multipart World!"
message["From"] = sender
message["To"] = receiver

### Attach message body content
message.attach(MIMEText("Hello from Python", "plain"))

### Attach image
filename = './assets/camera.jpeg'
with open(filename, "rb") as f:
    file = MIMEApplication(f.read())
disposition = f"attachment; filename={filename}"
file.add_header("Content-Disposition", disposition)
message.attach(file)


### If not sending plain text, use 'message.as_string()'
with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())

