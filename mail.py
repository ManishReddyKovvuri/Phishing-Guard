import imaplib
import email
from email.header import decode_header
import socket
from detection import fake_detect
from GetUrls import parse_email

# Account credentials
<<<<<<< HEAD
username = "phishguard.safe@gmail.com"#TODO
password = ""
=======
username = "manishrk2120@gmail.com"
password = "kdtn aqyl ofwe tddb"
>>>>>>> e0e7a5068024befa80ba835c66091ec284d288ee
imap_server = "imap.gmail.com"

# Connect to the server
try:
    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)
    
    # Log in to your account
    mail.login(username, password)
    
    # Select the mailbox you want to read from
    mail.select("inbox")
    
    # Search for all emails in the inbox
    status, messages = mail.search(None, "ALL")
    
    # Convert messages to a list of email IDs
    email_ids = messages[0].split()
    
    # Fetch the latest email
    latest_email_id = email_ids[-1]
    
    # Fetch the email by ID
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")


    
    # Parse the email content
    parse_email(msg_data)
    
    
    # Close the connection and logout
    mail.close()
    mail.logout()

except imaplib.IMAP4.error as e:
    print("IMAP error:", e)
except socket.gaierror as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
