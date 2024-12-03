import imaplib
import email
from email.header import decode_header
import socket
from detection import fake_detect
from GetUrls import parse_email, getUrls, add_urls_to_dict, generate_response_body, read_unread_emails
from helpers.url_helper import load_config
from helpers.models import ICloudEmail



try:
    config =load_config()
    # Account credentials
    username = config.get("EMAIL")
    password = config.get("PASS_KEY")
    imap_server = "imap.icloud.com"

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password) # Connect to the server

    
    
    
    

    
    unread_emails = read_unread_emails(mail) #list of ICloudEmail Objects 
    response_emails = {email.from_address: False for email in unread_emails}
    for email in unread_emails :
    # icloudemail = ICloudEmail()
    # icloudemail.from_address ="--@gmail.com"
    # icloudemail.subject = " babai"
    # icloudemail.body = "https://www.youtube.com/watch?v=23yVLxPvRfY, ahfdsgkajgflasfg  https://mail.google.com/mail/u/0/#inbox "# parse_email
    # print("="*50)
        email.urls_found["URLs"] = getUrls(email.body)
        for i in email.urls_found["URLs"] :
            email.urls_found["report"].append(fake_detect(i)) #TODO change parameter to fakedectecin object
            # responsebody= generate_response_body(email) # added directly into dict 
            response_emails[email.from_address]  = generate_response_body(email)
    
    #TODO send each response
    for email_address in response_emails:
        if response_emails[email_address] != False :
            #TODO send report 
            continue
        else :
            #TODO sorry cant read the body email
            continue
    # # Close the connection and logout
    # mail.close()
    # mail.logout()

    #TODO implement wait period
except imaplib.IMAP4.error as e:
    print("IMAP error:", e)
except socket.gaierror as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
