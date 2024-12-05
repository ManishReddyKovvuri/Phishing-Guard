from uuid import UUID
import os
from data import MODEL_DIR
from helpers import get_ssl_certificate, get_redirected_url, extract_url_features
from helpers.models import  FakeDetectionIn, FakeDetectionResponse
from urllib.parse import urlparse
import pickle
import re
import pandas as pd





def fake_detect(uuid_text):
    try :
        _dict = {}
        _dict["original_url"] = str(uuid_text)
        check, _original_url = get_redirected_url(str(uuid_text))
        if _original_url == "data:,":
            _original_url = uuid_text
        if not check:
            print(f"Selenium Could not load the Site 😞'{uuid_text}'") #TODO send the reason back to mail.py for template
            _original_url = uuid_text
        print(f"Redirect Found : '{uuid_text}'")
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

        response = FakeDetectionResponse.model_validate(_dict)
        # response.provide_recommendations()
        return (response)   
    
    except Exception as e:
        print( "exception found : ",e)
        return False #TODO  change two a flag object with reason

