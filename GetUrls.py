import re
import email
from email.header import decode_header
from detection import fake_detect
from helpers.models import FakeDetectionIn,FakeDetectionResponse
def getUrls(text):
    # Regular expression to match URLs
    url_pattern = re.compile(r'https?://[^\s]+')
    urls = url_pattern.findall(text)
    return urls

def add_urls_to_dict(urls):
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
                    
                    urls = getUrls(body)
                    url_dict = add_urls_to_dict(urls)
                    for i in url_dict:
                        url_dict[i] = fake_detect(FakeDetectionIn(uuid= 'e4eaaaf2c9b648b3b0e4b5b4b3a9a2bb', text= i))
                    return url_dict


# Extract URLs from the text


# Print the resulting dictionary
