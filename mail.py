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
import uuid
from helpers.logger import logger



try:
    logger.info("New Session ========================================================================================")
    config =load_config()
    logger.info(f"Loaded Info from Config File'")

    # Account credentials
    username = config.get("EMAIL")
    password = config.get("PASS_KEY")
    imap_server = "imap.mail.me.com"


    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password) # Connect to the server
    logger.info(f"Successfully connected to Imap_Server'")


    unread_emails = check_for_unread(mail) #list of icloud email objects
    if not unread_emails:
        logger.debug("No unread emails found. Ending execution.")
        raise Exception("No unread emails found. Ending execution.")
    else :
        logger.debug(f"Found Unread Emails : {len(unread_emails)}")

        
    # response_emails = {email.from_address: False for email in unread_emails} #TODO change the Dict key value ( if multiple emails are from same person(email id) it gets overwritten )
    response_emails = {str(uuid.uuid4()) : email for i, email in enumerate(unread_emails)}
 
    response_body = {}


    
    
    for id, email in response_emails.items() :
        logger.info(f"Processing URLS : {id}_{email.from_address} with subject '{email.subject}'")
        email.urls_found["URLs"] = getUrls(email.body)

        # logger.debug(f"URLS Found for {id}_{email.from_address} : {k}")
        for i in email.urls_found["URLs"] :
            logger.debug(f"Processing report for URL : {i}  within the email {id}_{email.from_address}")
            email.urls_found["report"].append(fake_detect(i)) #TODO change parameter to fakedectecin object
            # responsebody= generate_response_body(email) # added directly into dict 
        # response_emails[id]  = generate_response_body(email)
        response_body[id]  = generate_response_body(email)

    smtp_server = 'smtp.mail.me.com'
    smtp_port = 587
    smtp_user = config.get("EMAIL")
    smtp_password = config.get("PASS_KEY")
    from_email = config.get("FROM")

    logger.debug(f"Connecting to SMTP SERVER")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    logger.debug(f"Login Successful")


    for id, email in response_emails.items():
        if response_body[id]:
            to_email = response_emails[id].from_address
            subject = response_emails[id].subject
            body = response_body[id]
            


            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # Send the email
            
            server.send_message(msg)
            logger.debug(f"mail sent to {to_email} from  {from_email} Successfully.")
            
            #TODO send report 
            continue
        else :
            #TODO sorry cant read the body email
            continue

    server.quit()
    #TODO implement wait period
except imaplib.IMAP4.error as e:
    logger.error("IMAP error:", e, exc_info=True)
except socket.gaierror as e:
    logger.error("Socket error:", e, exc_info=True)
except Exception as e:
    logger.error("Error:", exc_info= True)
finally:
    logger.info("Session completed ========================================================================================")

