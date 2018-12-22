# py-pgpmail
##### Simple wrapper to send pgp mails over smtp
######How to Use


1. Import PGP Keys (gpg --keyserver keyserver.cybernation.eu --recv KEY_ID )
2. Send PGP Mail via Python
```python
if __name__ == "__main__":
    send_smtp_pgp_mail("mail.riseup.net", "webmaster@riseup.net", 
    "securePassword;)", "Webmaster<webmaster@cybernation.eu>",
     "THIS TEXT WILL BE ENCRYPTED", server_port=465)

```