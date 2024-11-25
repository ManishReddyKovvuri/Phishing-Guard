import whois
from datetime import datetime
import tldextract
from urllib.parse import urlparse
import urllib
import re
import requests
import json,os  



def get_domain_age(domain_name: str) -> int:
    try:
        # Perform a WHOIS lookup for the domain
        domain_info = whois.whois(domain_name)

        # Extract the creation date from the WHOIS information
        creation_date = domain_info.creation_date

        # Ensure that creation_date is a datetime object
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # Calculate the domain age
        current_date = datetime.now()
        domain_age = current_date - creation_date
        return domain_age.days
    except Exception as e:
        # Return -1 if domain age is not available
        return -1
def load_config():
    file_name = "config.json"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "..", file_name)
    try:
        with open(config_path, "r") as file:
           return  json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {config_path} was not found.")
        return{}
    except json.JSONDecodeError:
        print(f"Error: The file {config_path} is not a valid JSON file.")
        return{}

def page_rank(url: str) -> int:
    o = urllib.parse.urlsplit(url)
    url_to_check = o[1]
    config = load_config()
    # Make a GET request to the Open PageRank API
    url1 = 'https://openpagerank.com/api/v1.0/getPageRank'
    params = {
        'domains[]': url_to_check
    }
    headers = {
        'API-OPR': config.get('API_OPR')
    }

    response = requests.get(url1, params=params, headers=headers)
    data = response.json()

    return data['response'][0]['page_rank_decimal']


# Function to extract features from a URL
def extract_url_features(url):
    parsed_url = urlparse(url)

    # Initialize a dictionary to store the features
    features = {'length_url': len(url), 'length_hostname': len(parsed_url.netloc)}

    # Feature: IP Address (True if the hostname is an IP address, False otherwise)
    a1 = parsed_url.netloc.replace('.', '').isdigit()
    if a1 == "True":
        features["ip"] = 1
    else:
        features["ip"] = 0

    # Feature: Number of dots in the URL
    features['nb_dots'] = url.count('.')

    # Feature: Number of question marks in the URL
    features['nb_qm'] = url.count('?')

    # Feature: Number of equal signs in the URL
    features['nb_eq'] = url.count('=')

    # Feature: Number of slashes in the URL
    features['nb_slash'] = url.count('/')

    # Feature: Number of 'www' subdomains
    features['nb_www'] = parsed_url.netloc.count('www')

    # Feature: Ratio of digits in the URL
    try:
        features['ratio_digits_url'] = sum(c.isdigit() for c in url) / len(url)
    except Exception as e:
        features['ratio_digits_url'] = 0

    # Feature: Ratio of digits in the hostname
    try:
        features['ratio_digits_host'] = sum(c.isdigit() for c in parsed_url.netloc) / len(parsed_url.netloc)
    except Exception as e:
        features['ratio_digits_host'] = 0

    # Feature: TLD (Top-Level Domain) in the subdomain
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain + '.' + extracted_domain.suffix
    tld = extracted_domain.suffix
    subdomain = extracted_domain.subdomain
    if subdomain.count(tld) > 0:
        features['tld_in_subdomain'] = 1
    else:
        features['tld_in_subdomain'] = 0

    # Feature: Prefix and Suffix in the hostname
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        features['prefix_suffix'] = 1
    else:
        features['prefix_suffix'] = 0

    # Feature: Length of the shortest word in the hostname
    words = parsed_url.netloc.split('.')
    features['shortest_word_host'] = min(len(word) for word in words)

    # Feature: Length of the longest words in the URL
    features['longest_words_raw'] = max(len(word) for word in url.split('/'))

    # Feature: Length of the longest word in the path
    path = parsed_url.path
    features['longest_word_path'] = max(len(word) for word in path.split('/'))

    # Feature: Phishing hints (You can implement a specific algorithm to detect phishing hints)
    _hints = ['wp', 'login', 'includes', 'admin', 'content', 'site', 'images', 'js', 'alibaba', 'css', 'myaccount',
              'dropbox', 'themes', 'plugins', 'signin', 'view']
    path = parsed_url.path
    c = 0
    for hint in _hints:
        c += path.lower().count(hint)
    features["phish_hints"] = c

    # Feature: Domain Age (You can implement a function to retrieve the domain age)

    features["domain_age"] = get_domain_age(parsed_url.netloc)

    # Feature: Page Rank (You can implement a function to retrieve the page rank)
    features["page_rank"] = float(page_rank(url))

    return features
