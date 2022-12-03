import tkinter as tk # GUI
import smtplib  # Mail server 
import ssl  # Mail encryption 
from email.mime.application import MIMEApplication  # Mail message
from email.mime.text import MIMEText    # Mail message
from email.mime.multipart import MIMEMultipart  # Mail message

# ref for creating entry box with tkinter
# https://datatofish.com/entry-box-tkinter/

### Global variables for mail
CTX = ssl.create_default_context()
PWD = "pfsakavhmoalgkbr"    # Your app PWD goes here
SENDER = "realbirdproject@gmail.com"    # Your e-mail address


### Main Program

root= tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Send you an email with image')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Enter your email:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Entry(root) 
canvas1.create_window(200, 140, window=entry1)

# Function for sending mails
def send_email():
    receiver = entry1.get()

    ### Create the message
    message = MIMEMultipart("mixed")
    message["Subject"] = "Email send from GUI!"
    message["From"] = SENDER
    message["To"] = receiver

    ### Attach message body content
    message.attach(MIMEText("Hello from Real Birds", "plain"))

    ### Attach image       
    filename = './assets/camera.jpeg'   # Now the image is from asset folder. 
                                        # We should generate an image with GoPro pics & OpenCV & send it to user
    with open(filename, "rb") as f:
        file = MIMEApplication(f.read())
    disposition = f"attachment; filename={filename}"
    file.add_header("Content-Disposition", disposition)
    message.attach(file)

    ### If not sending plain text, use 'message.as_string()'
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=CTX) as server:
        server.login(SENDER, PWD)
        server.sendmail(SENDER, receiver, message.as_string())
    
    label3 = tk.Label(root, text='Email sent to ' + receiver, font=('helvetica', 10))
    canvas1.create_window(200, 210, window=label3)
    
button1 = tk.Button(text='Send the email', command=send_email, bg='brown', fg='black', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)

root.mainloop()