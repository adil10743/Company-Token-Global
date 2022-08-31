import smtplib
import os

from_addr = "" #sender address
Password = os.getenv("GmailPassword")

to_addr = "" #receiver address
cc = []
bcc = []
to_addrs = [to_addr] + cc + bcc



def email(SUBJECT, TEXT):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) #smtplib.SMTP('smtp.office365.com', 587) #
        server.starttls()
        server.login(from_addr, Password)
        message = "From: %s\r\n" % from_addr + "To: %s\n" % to_addr + "CC: %s\n" % ",".join(cc) + "Subject: %s\n" % SUBJECT + "\n" + TEXT

        server.sendmail(from_addr, to_addrs, message)
        server.quit()
        print('Mail sent')
    except Exception as e: 
        print(e)

def main():
    email("Test", "Hello there")
