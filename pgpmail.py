import re
import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import gnupg


class MIMEApplicationPGPPayload(MIMEApplication):
    def __init__(self, _data,
                 _subtype='octet-stream; name="encrypted.asc"',
                 _encoder=encoders.encode_noop,
                 **_params):
        _params["Content-Description"] = "OpenPGP encrypted message"
        _params["Content-Disposition"] = 'inline; filename="encrypted.asc"'
        MIMEApplication.__init__(self, _data=_data, _subtype=_subtype,
                                 _encoder=_encoder, **_params)


class MIMEApplicationPGPDescription(MIMEApplication):
    def __init__(self, _data="Version: 1\n", _subtype='pgp-encrypted',
                 _encoder=encoders.encode_noop,
                 **_params):
        _params["Content-Description"] = "PGP/MIME version identification"
        MIMEApplication.__init__(self, _data=_data, _subtype=_subtype,
                                 _encoder=_encoder, **_params)


class MIMEMultipartPGP(MIMEMultipart):
    def __init__(self, _data=None, _subtype='encrypted', boundary=None,
                 **_params):
        _params['protocol'] = "application/pgp-encrypted"
        description = MIMEApplicationPGPDescription()
        payload = MIMEApplicationPGPPayload(_data)
        _subparts = [description, payload]
        MIMEMultipart.__init__(self, _subtype=_subtype, boundary=boundary,
                               _subparts=_subparts, **_params)


def send_smtp_pgp_mail(server_address, username, password, recp, subject, msg, sender=None, server_port=25):
    ssl = None
    smtp_server = None

    if sender == None:
        sender = username

    gpg = gnupg.GPG()
    gpg_obj = ""

    if "<" in recp:
        gpg_obj = gpg.encrypt(msg, re.findall("<\S{1,}>", recp)[0][1:-1])
    else:
        gpg_obj = gpg.encrypt(msg, recp)

    if not gpg_obj.status == 'encryption ok':
        raise Exception("Sent PGP Error: " + gpg_obj.status)

    if server_port == 465:
        # Initialize SSL Connection
        smtp_server = smtplib.SMTP_SSL(server_address, server_port)
    else:
        # Initialize Unsecure Connection
        smtp_server = smtplib.SMTP(server_address, server_port)

    smtp_server.login(username, password)

    msg = MIMEMultipartPGP(gpg_obj.data)

    msg['Subject'] = subject
    msg["From"] = sender
    msg["To"] = recp
    smtp_server.send_message(msg)
