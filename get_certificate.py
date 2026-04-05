import ssl

cert_pem = ssl.get_server_certificate(("unifi.local", 443))
with open("local_unifi.crt", "w") as f:
    f.write(cert_pem)