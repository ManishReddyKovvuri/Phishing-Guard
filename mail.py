import imaplib
import email
from email.header import decode_header
import socket
from detection import fake_detect
from GetUrls import parse_email, getUrls,check_for_unread, add_urls_to_dict, generate_response_body, read_unread_emails
from helpers.url_helper import load_config
from helpers.models import ICloudEmail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



try:
    config =load_config()
    # Account credentials
    username = config.get("EMAIL")
    password = config.get("PASS_KEY")
    imap_server = "imap.mail.me.com"

    unread_email_found = False #set to true to check

    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password) # Connect to the server

    unread_emails = check_for_unread(mail)
    if not unread_emails:
        print("No unread emails found. Ending execution.")
        raise Exception("No unread emails found. Ending execution.")
        
    response_emails = {email.from_address: False for email in unread_emails} #TODO change the Dict key value ( if multiple emails are from same person(email id) it gets overwritten )
    


    
    
    for email in unread_emails :
        email.urls_found["URLs"] = getUrls(email.body)
        for i in email.urls_found["URLs"] :
            email.urls_found["report"].append(fake_detect(i)) #TODO change parameter to fakedectecin object
            # responsebody= generate_response_body(email) # added directly into dict 
            response_emails[email.from_address]  = generate_response_body(email)
            #print(generate_response_body(email))
    
    #TODO send each response
    for email_address in response_emails:
        if response_emails[email_address] != False :
            smtp_server = 'smtp.mail.me.com'
            smtp_port = 587
            smtp_user = config.get("EMAIL")
            smtp_password = config.get("PASS_KEY")

            from_email = config.get("FROM")
            to_email = email_address
            subject = email.subject
            body=email.response_email_body
            


            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # Send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print("mail sent")
            server.quit()
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
