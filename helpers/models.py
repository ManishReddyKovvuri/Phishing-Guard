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


class FakeDetectionIn(BaseModel):
    uuid: UUID
    text: str
