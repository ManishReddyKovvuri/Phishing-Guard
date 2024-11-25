from typing import List, Optional, Annotated, Any, Dict
from uuid import UUID

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
    Recommendation : List[ str]
    def provide_recommendations(self):
        isSSLAvailable = self.ssl_cert.isSSLAvailable
        if self.features.length_url > 100:
            self.Recommendation.append("The URL is very long, which can be suspicious.")
        if self.features.nb_eq > 3:
            self.Recommendation.append("The URL has multiple '=' characters, which can indicate phishing.")
        if self.features.ratio_digits_url > 0.2:
            self.Recommendation.append("The URL has a high ratio of digits, which can be suspicious.")
        if not isSSLAvailable:
            self.Recommendation.append("The URL does not have a valid SSL certificate.")
        if self.features.domain_age < 365:
            self.Recommendation.append("The domain is less than a year old, which can be a red flag.")
        if self.features.page_rank == 0.0:
            self.Recommendation.append("The URL has a low page rank, indicating it might be untrustworthy.")
        if self.ModelPrediction == 'Fake':
           self.Recommendation.append("The machine learning model predicts this URL to be fake.")
        
        if not self.Recommendation:
            self.Recommendation.append("The URL appears to be safe based on the analyzed features.")




class FakeDetectionIn(BaseModel):
    uuid: UUID
    text: str


class ICloudEmail():
    def __init__(self, from_address: str ='', subject: str='', body: str=''):
        self.from_address = from_address
        self.subject = subject
        self.body = body
        self.urls_found = {
            "URLs": [],
            "report": [FakeDetectionResponse]
        }
        



