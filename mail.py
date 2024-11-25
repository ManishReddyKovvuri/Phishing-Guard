import imaplib
import email
from email.header import decode_header
import socket
from detection import fake_detect
from GetUrls import parse_email
from helpers.url_helper import load_config


config =load_config()
# Account credentials
<<<<<<< HEAD
username = ""
password = ""
imap_server = "imap.mail.me.com"
=======
username = config.get("EMAIL")
password = config.get("PASS_KEY")
imap_server = "imap.gmail.com"
>>>>>>> ea3b315d11b7c2f2d02c875b6b009b6b9af21d28

# Connect to the server
try:
    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)
    print("Connected to the server")

    # Login to your iCloud account
    mail.login(username,password)
    print("Logged in successfully")

    # Select the mailbox (in this case, the inbox)
    status, messages = mail.select("inbox")
    if status != 'OK':
        print("Failed to select inbox")
        raise Exception("Failed to select inbox")
    print("Inbox selected")

    # Search for all emails in the inbox
    status, messages = mail.search(None, "ALL")
    if status != 'OK':
        print("Failed to search inbox")
        raise Exception("Failed to search inbox")
    print(f"Search status: {status}")

    # Get the list of email IDs
    email_ids = messages[0].split()
    if not email_ids:
        print("No emails found")
        raise Exception("No emails found")
    print(f"Number of emails: {len(email_ids)}")
    
    # Convert messages to a list of email IDs
    status, msg_data = mail.fetch(email_ids[-1], "(RFC822)")
    if status != 'OK':
        raise Exception("Failed to fetch email")
    print("Email fetched successfully")
    
    # Fetch the latest email


    
    # Parse the email content
    report = parse_email(msg_data)
    print(report)
    
    
    # Close the connection and logout
    mail.close()
    mail.logout()

except imaplib.IMAP4.error as e:
    print("IMAP error:", e)
except socket.gaierror as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
