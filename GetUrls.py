import re
import email
from email.header import decode_header
from detection import fake_detect
from helpers.models import FakeDetectionIn,FakeDetectionResponse, ICloudEmail


def getUrls(text):
    # Regular expression to match URLs
    url_pattern = re.compile(r'https?://[^\s]+') #TODO r"https?://\S+|www\.\S+|ftp://\S+|\S+\.\S+/\S+" 
    urls = url_pattern.findall(text)
    return urls

def add_urls_to_dict(urls):  #TODO remove
    # Initialize an empty dictionary
    url_dict = {}
    for url in urls:
        url_dict[url] = False
    return url_dict

def parse_email(msg_data):
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
                        urls = getUrls(body)
                        url_dict = add_urls_to_dict(urls)
                        for i in url_dict:
                            url_dict[i] = fake_detect(FakeDetectionIn(uuid= 'e4eaaaf2c9b648b3b0e4b5b4b3a9a2bb', text= i))
                        return url_dict
                    
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
                    
                    # urls = getUrls(body)
                    # url_dict = add_urls_to_dict(urls)
                    # for i in url_dict:
                    #     url_dict[i] = fake_detect(FakeDetectionIn(uuid= 'e4eaaaf2c9b648b3b0e4b5b4b3a9a2bb', text= i))
                    # return url_dict

def check_for_unread(mail):
    """Check for unread emails and return a list of email objects."""
    try:
        mail.select("inbox")  # Select the inbox
        status, messages = mail.search(None, "UNSEEN")
        if messages == [b'']:  # No unread emails
            print("No unread emails found.")
            return []

        email_ids = messages[0].split()
        unread_emails = []
        for email_id in email_ids:
            email_obj = read_unread_emails(mail=mail, email_id=email_id)
            if email_obj:  # Only append if processing succeeded
                unread_emails.append(email_obj)
        return unread_emails

    except Exception as e:
        print(f"Error in checking for unread emails: {e}")
        return []

def read_unread_emails(mail, email_id):
    """Fetch and read a single unread email."""
    try:
        email_id = email_id.decode()  # Decode the email ID
        print(f"Fetching email ID: {email_id}")

        # Fetch the full email content
        status, msg_data = mail.fetch(email_id, "(BODY[])")
        if not msg_data or msg_data[0] == b'' or b'()' in msg_data[0]:
            print(f"No content found for email ID {email_id}. Skipping.")
            return False

        raw_email = b''.join(
            response_part[1] for response_part in msg_data if isinstance(response_part, tuple)
        )

        if not raw_email:
            print(f"No content found for email ID {email_id}. Skipping.")
            return False

        # Parse the email
        msg = email.message_from_bytes(raw_email)

        # Decode the subject
        try:
            subject_raw = msg.get("Subject")
            if subject_raw:
                subject, encoding = decode_header(subject_raw)[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
            else:
                subject = "(No Subject)"
        except Exception as e:
            print(f"Error decoding subject for email {email_id}: {e}")
            subject = "(Error Reading Subject)"

        # Decode the from address
        try:
            from_address = msg.get("From") or "(Unknown Sender)"
        except Exception as e:
            print(f"Error decoding 'From' address for email {email_id}: {e}")
            from_address = "(Error Reading Sender)"

        # Decode the body
        try:
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode(errors='replace')
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors='replace')
            if not body:
                body = "(No Body Content)"
        except Exception as e:
            print(f"Error decoding body for email {email_id}: {e}")
            body = "(Error Reading Body)"

        print("/=\//" * 50)
        print(f"Subject: {subject}")
        print(f"From: {from_address}")
        print(f"Body:\n{body}\n")
        print("=" * 50)

        # Create and return the email object
        icloudemail = ICloudEmail()
        icloudemail.body = body
        icloudemail.subject = subject
        icloudemail.from_address = from_address
        return icloudemail

    except Exception as e:
        print(f"Error reading email {email_id}: {e}")
        return False

def generate_response_body(icloud_email: ICloudEmail) -> str:
    """
    Generates a response email body based on the URLs found and their analysis.
    :param icloud_email: An instance of ICloudEmail containing URLs and reports.
    :return: A string representing the email body.
    """
    try :
        # Initialize the email body
        response_body = f"Subject: {icloud_email.subject}\n"
        response_body += f"From: {icloud_email.from_address}\n\n"
        response_body += f"Hello,\n\nWe have analyzed the email body and found the following results:\n\n"

        if not icloud_email.urls_found["URLs"]:
            response_body += "No URLs were found in the email body. The content seems safe.\n"
        else:
            response_body += f"We identified {len(icloud_email.urls_found['URLs'])} link(s) in the email body:\n\n"
            
            for i, (url, report) in enumerate(zip(icloud_email.urls_found["URLs"], icloud_email.urls_found["report"]), start=1):
                # Generate recommendations for the current URL
                report.provide_recommendations()

                # Add URL details to the response body
                response_body += f"Link {i}: {url}\n"
                response_body += f"    Expanded URL: {report.long_url}\n"
                response_body += f"    SSL Certificate: {'Valid' if report.ssl_cert.isSSLAvailable else 'Invalid'}\n"
                response_body += f"    Host Name: {report.host_name}\n"
                response_body += f"    Port: {report.port}\n"
                response_body += f"    Model Prediction: {report.ModelPrediction}\n"
                response_body += f"    Security Features:\n"
                response_body += f"        URL Length: {report.features.length_url}\n"
                response_body += f"        '=' Characters: {report.features.nb_eq}\n"
                response_body += f"        Digit Ratio: {report.features.ratio_digits_url}\n"
                response_body += f"        Domain Age: {report.features.domain_age} days\n"
                response_body += f"        Page Rank: {report.features.page_rank}\n\n"

                # Add recommendations for the URL
                response_body += f"    Recommendations:\n"
                for recommendation in report.Recommendation:
                    response_body += f"        - {recommendation}\n"
                response_body += "\n"
        
        response_body += "Thank you for using our phishing detection service.\n"
        response_body += "Stay safe,\nThe Phishing Guard Team"

        # Assign the generated response to the email body attribute
        icloud_email.response_email_body = response_body
        return response_body
    except :
        return False
