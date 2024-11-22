import re

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



# Extract URLs from the text


# Print the resulting dictionary
