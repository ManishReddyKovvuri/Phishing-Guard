import imaplib
import email
from email.header import decode_header
import socket
from detection import detect
from GetUrls import getUrls, add_urls_to_dict

# Account credentials
username = "phishguard.safe@gmail.com"
password = ""
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
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            from_ = msg.get("From")
            print("Subject:", subject)
            print("From:", from_)
    
            # If the email message is multipart
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/html":
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            continue
                        
                        # Process HTML content
                        result = detect(body)
                        print("from detect (HTML):", result)
                        urls = getUrls(result)
                        url_dict = add_urls_to_dict(urls)
                        print(url_dict)
                    
                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            with open(filename, "wb") as f:
                                f.write(part.get_payload(decode=True))
            else:
                content_type = msg.get_content_type()
                if content_type == "text/html":
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        continue
                    
                    # Process HTML content
                    result = detect(body)
                    print("from detect (HTML non-multipart):", result)
                    urls = getUrls(result)
                    url_dict = add_urls_to_dict(urls)
                    print(url_dict)
    
    # Close the connection and logout
    mail.close()
    mail.logout()

except imaplib.IMAP4.error as e:
    print("IMAP error:", e)
except socket.gaierror as e:
    print("Socket error:", e)
except Exception as e:
    print("Error:", e)
