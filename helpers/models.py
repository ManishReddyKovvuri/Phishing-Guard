from typing import List, Optional, Annotated, Any, Dict
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, AfterValidator, model_validator, HttpUrl


def check_client(client: str):
    _allowed_clients = ["App", "Website"]
    assert client in _allowed_clients
    return client


class UserCreationIn(BaseModel):
    name: str
    client: Annotated[str, AfterValidator(check_client)]
    bot_token: Optional[str] = None
    telegram_user_id: Optional[str] = None

    @model_validator(mode='after')
    def check_tg_token_userid(self) -> Any:
        if self.client == "App":
            if self.bot_token is None and self.telegram_user_id is None:
                raise ValueError('For Client Type "Application" You Need to provide Telegram Bot Token and '
                                 'Telegram'
                                 'User ID')
        return self


class UserCreationResponse(BaseModel):
    session_uuid: UUID


class UserGet(BaseModel):
    uuid: str
    name: str
    telegram_user_id: str


class UsersGetAll(BaseModel):
    sessions_available: List[UserGet]


class SSLCert(BaseModel):
    isSSLAvailable: bool
    SSLPullError: str
    Certificate: Optional[Dict]


class URLFeatures(BaseModel):
    length_url: int
    length_hostname: int
    ip: int
    nb_dots: int
    nb_qm: int
    nb_eq: int
    nb_slash: int
    nb_www: int
    ratio_digits_url: float
    ratio_digits_host: float
    tld_in_subdomain: int
    prefix_suffix: int
    shortest_word_host: int
    longest_words_raw: int
    longest_word_path: int
    phish_hints: int
    domain_age: int
    page_rank: float


class FakeDetectionResponse(BaseModel):
    original_url: str
    long_url: str
    ssl_cert: SSLCert
    features: URLFeatures
    host_name: str
    port: int
    ModelPrediction: str
    Recommendation : List[ str] =[]
    def provide_recommendations(self):


        self.Recommendation = []

        # High Priority: SSL Certificate Check
        if not self.ssl_cert.isSSLAvailable:
            self.Recommendation.append("The URL does not have a valid SSL certificate, which may indicate it is insecure.")
        else:
            cert_expiration = self.ssl_cert.Certificate["notAfter"]
            if cert_expiration and datetime.strptime(cert_expiration, '%m/%d/%Y') < datetime.now():
                self.Recommendation.append("The SSL certificate for this site has expired.")

        # Domain Reputation
        if self.features.page_rank > 4:
            # Reputable sites can tolerate longer URLs or more digits
            relaxed_url_length_threshold = 500
            relaxed_eq_threshold = 10
            relaxed_digit_ratio = 0.3
        else:
            # Strict thresholds for less-known sites
            relaxed_url_length_threshold = 100
            relaxed_eq_threshold = 3
            relaxed_digit_ratio = 0.2

        # Medium Priority: URL Features
        if self.features.length_url > relaxed_url_length_threshold:
            self.Recommendation.append("The URL is very long, which can be suspicious.")
        if self.features.nb_eq > relaxed_eq_threshold:
            self.Recommendation.append("The URL contains multiple '=' characters, which is unusual and may indicate phishing.")
        if self.features.ratio_digits_url > relaxed_digit_ratio:
            self.Recommendation.append("The URL has a high ratio of digits, which can be suspicious.")

        # Low Priority: Domain Age
        if self.features.domain_age < 365:
            self.Recommendation.append("The domain is less than a year old, which can be a red flag.")

        # Add Model Prediction
        if self.ModelPrediction == "Fake":
            self.Recommendation.append("The machine learning model predicts this URL to be malicious.")

        # Default Safe Message
        if not self.Recommendation:
            self.Recommendation.append("The URL appears safe based on the analyzed features.")

    
class FakeDetectionIn(BaseModel):
    uuid: UUID
    text: str


class ICloudEmail():
    def __init__(self, from_address: str ='', subject: str='', body: str='', sent_time= datetime):
        self.from_address = from_address
        self.subject = subject
        self.body = body
        self.sent_time= sent_time
        
        self.urls_found = {
            "URLs": [],
            "report": []#TODO default to false
        }
        



