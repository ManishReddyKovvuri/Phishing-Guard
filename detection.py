from uuid import UUID
import os
from data import MODEL_DIR
from helpers import get_ssl_certificate, get_redirected_url, extract_url_features
from helpers.models import  FakeDetectionIn, FakeDetectionResponse
from urllib.parse import urlparse
import pickle
import re
import pandas as pd



class Config(object):
    OPEN_PAGE_RANK_API_KEY = os.environ.get("OPEN_PAGE_RANK_API_KEY", "--") # load api key from config file
    API_KEY = os.environ.get("API_KEY", "test")


def fake_detect(uuid_text: FakeDetectionIn):
    url_pattern = r"https?://\S+|www\.\S+|ftp://\S+|\S+\.\S+/\S+"
    uuid_text.text = re.findall(url_pattern, uuid_text.text)
    if uuid_text.text is None:
        raise HTTPException(status_code=404, detail={"Could not find URL in the text you sent"})
    uuid_text.text = uuid_text.text[0]
    _dict = {}
    _dict["original_url"] = str(uuid_text.text)
    check, _original_url = get_redirected_url(str(uuid_text.text))
    if _original_url == "data:,":
        _original_url = uuid_text.text
    if not check:
        print(f"Selenium Could not load the Site 😞'{uuid_text.text}'")
        _original_url = uuid_text.text
    print(f"Redirect Found : '{uuid_text.text}'")
    _dict["long_url"] = _original_url 
    parsed_hostname = urlparse(_original_url).netloc
    parsed_port = urlparse(_original_url).port
    if parsed_port is None:
        parsed_port = 443
    check, err, cert = get_ssl_certificate(parsed_hostname, parsed_port, timeout=10)
    _dict["ssl_cert"] = {
        "isSSLAvailable": check,
        "SSLPullError": err,
        "Certificate": cert
    }
    if cert is not None:
        _dict["ssl_cert"]["Certificate"]["notBefore"] = _dict["ssl_cert"]["Certificate"]["notBefore"].strftime('%m/%d/%Y')
        _dict["ssl_cert"]["Certificate"]["notAfter"] = _dict["ssl_cert"]["Certificate"]["notAfter"].strftime('%m/%d/%Y')

    
    _features = extract_url_features(_original_url)
    _dict["features"] = _features

    _dict["host_name"] = parsed_hostname
    _dict["port"] = parsed_port
    X = pd.DataFrame(_features, index=[0]).iloc[:, :].values
    with open(MODEL_DIR, 'rb') as model:
        _model = pickle.load(model)
    _pred = _model.predict(X)


    _dict["ModelPrediction"] = "Legit Site" if _pred == 0 else "Fake"
    response = FakeDetectionResponse.parse_obj(_dict)
    return (response)




fake_detection_input = FakeDetectionIn(
    uuid= 'e4eaaaf2c9b648b3b0e4b5b4b3a9a2bb',  # Generate a new UUID
    text= "http://usaa.fmvela.mx"
)

fake_detect(fake_detection_input)