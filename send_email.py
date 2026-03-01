import smtplib

def send_mail(email, password, receiver_email, message):
    sender = f"Your Name <{email}>"
    receiver = f"Recipient <{receiver_email}>"
    
    m = f"""\
Subject: Test Email from Python
To: {receiver}
From: {sender}

Hello!

"""
    m += message
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email, password)
        server.sendmail(sender, receiver, m)
        print("✅ Email sent successfully!")

# ===== EDIT THESE 4 LINES =====
my_email = "sender@gmail.com"              # Your Gmail address
my_password = "xxxx xxxx xxxx xxxx"           # Your 16-char App Password
recipient = "receiver@gmail.com"           # Who receives the email
msg = "This is a email mafia from Python anna!"    # Your message
# ==============================

# Send the email
send_mail(my_email, my_password, recipient, msg)