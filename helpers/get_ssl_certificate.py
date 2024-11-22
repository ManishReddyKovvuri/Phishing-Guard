import ssl
import socket
from socket import gaierror
import OpenSSL
from datetime import datetime
from ssl import SSLCertVerificationError, SSLError


def get_ssl_certificate(host, port=443, timeout=10) -> (bool, str):
    flag = True
    err = ""
    gai_flag = False
    try:
        context = ssl.create_default_context()
        conn = socket.create_connection((host, port))
        sock = context.wrap_socket(conn, server_hostname=host)
        flag = True
    except SSLCertVerificationError as e:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        flag = False
        err = str(e)
    except SSLError as e:
        flag = False
        err = str(e)
        gai_flag = True
    except gaierror as e:
        flag = False
        err = str(e)
        gai_flag = True
    finally:
        if gai_flag:
            return flag, err, None
        conn = socket.create_connection((host, port))
        sock = context.wrap_socket(conn, server_hostname=host)
        sock.settimeout(timeout)
        der_cert = sock.getpeercert(True)
        _cert = ssl.DER_cert_to_PEM_cert(der_cert)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, _cert)
        subject = x509.get_subject().get_components()
        issuer = x509.get_issuer().get_components()
        result = {
            'subject': {key.decode('utf-8'): value.decode('utf-8') for key, value in subject},
            'issuer': {key.decode('utf-8'): value.decode('utf-8') for key, value in issuer},
            'serialNumber': x509.get_serial_number(),
            'version': x509.get_version(),
            'notBefore': datetime.strptime(x509.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ'),
            'notAfter': datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ'),
        }

        extensions = (x509.get_extension(i) for i in range(x509.get_extension_count()))
        extension_data = {e.get_short_name().decode('utf-8'): str(e) for e in extensions}
        result.update(extension_data)
        sock.close()
        return flag, err, result



