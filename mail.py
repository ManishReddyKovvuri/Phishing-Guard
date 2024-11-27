import imaplib
import email
from email.header import decode_header
import socket
from detection import fake_detect
from GetUrls import parse_email, getUrls, add_urls_to_dict, generate_response_body, read_unread_emails
from helpers.url_helper import load_config
from helpers.models import ICloudEmail


config =load_config()
# Account credentials
username = config.get("EMAIL")
password = config.get("PASS_KEY")
imap_server = "imap.gmail.com"

# Connect to the server
try:
    # # Connect to the Gmail IMAP server
    # mail = imaplib.IMAP4_SSL(imap_server)
    # print("Connected to the server")

    # # Login to your iCloud account
    # mail.login(username,password)
    # print("Logged in successfully")

    # # Select the mailbox (in this case, the inbox)
    # status, messages = mail.select("inbox")
    # if status != 'OK':
    #     print("Failed to select inbox")
    #     raise Exception("Failed to select inbox")
    # print("Inbox selected")

    # # Search for all emails in the inbox
    # status, messages = mail.search(None, "ALL")
    # if status != 'OK':
    #     print("Failed to search inbox")
    #     raise Exception("Failed to search inbox")
    # print(f"Search status: {status}")

    # # Get the list of email IDs
    # email_ids = messages[0].split()
    # if not email_ids:
    #     print("No emails found")
    #     raise Exception("No emails found")
    # print(f"Number of emails: {len(email_ids)}")
    
    # # Convert messages to a list of email IDs
    # status, msg_data = mail.fetch(email_ids[-1], "(RFC822)")
    # if status != 'OK':
    #     raise Exception("Failed to fetch email")
    # print("Email fetched successfully")

    # # Parse the email content
    # report = parse_email(msg_data)
    # print(report)

    
    
    
    # # Close the connection and logout
    # mail.close()
    # mail.logout()

    
    unread_emails = read_unread_emails(mail) #list of ICloudEmail Objects 
    response_emails = {email.from_address: False for email in unread_emails}
    for email in unread_emails :
    # icloudemail = ICloudEmail()
    # icloudemail.from_address ="--@gmail.com"
    # icloudemail.subject = " babai"
    # icloudemail.body = "https://www.youtube.com/watch?v=23yVLxPvRfY, ahfdsgkajgflasfg  https://mail.google.com/mail/u/0/#inbox "# parse_email
    # print("="*50)
        email.urls_found["URLs"] = getUrls(icloudemail.body)
        for i in email.urls_found["URLs"] :
            email.urls_found["report"].append(fake_detect(i))
            # responsebody= generate_response_body(email) # added directly into dict 
            response_emails[email.from_address]  = generate_response_body(email)
    
    # send each response
    for email_address in response_emails:
        if response_emails[email_address] != False :
            continue

except imaplib.IMAP4.error as e:
    print("IMAP error:", e)
except socket.gaierror as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
