#!/bin/bash

mkdir test/certs

# The 'good' ca  cert
openssl req -new -x509  -keyout test/certs/cakey.pem -out test/certs/cacert.pem -days 365 -passout pass:fakepassword -subj "/C=US/ST=WA/L=Seattle/O=FakeTestingOrg/CN=fakeca.test"

# The 'good' server cert
openssl req -out test/certs/server_req.pem -new -newkey rsa:4096 -nodes -keyout test/certs/server_key.pem -subj "/C=US/ST=WA/L=Seattle/O=FakeTestingOrg/CN=localhost"
openssl x509 -req -days 365 -passin pass:fakepassword -in test/certs/server_req.pem -CA test/certs/cacert.pem -CAkey test/certs/cakey.pem -out test/certs/server-cert.pem -CAcreateserial -extfile <(printf "[SAN]\nsubjectAltName=DNS:localhost") -extensions SAN

# A client cert using the same ca
openssl req -out test/certs/client_req.pem -new -newkey rsa:4096 -nodes -keyout test/certs/client_key.pem -subj "/C=US/ST=WA/L=Seattle/O=FakeTestingOrg/CN=my.app"
openssl x509 -req -days 365 -passin pass:fakepassword -in test/certs/client_req.pem -CA test/certs/cacert.pem -CAkey test/certs/cakey.pem -out test/certs/client-cert.pem -CAcreateserial -extfile <(printf "[SAN]\nsubjectAltName=DNS:my.app") -extensions SAN

# The 'bad' cert that our tests can't validate
openssl req -new -x509  -keyout test/certs/cakey2.pem -out test/certs/cacert2.pem -days 365 -passout pass:fakepassword -subj "/C=US/ST=WA/L=Seattle/O=FakeTestingOrg/CN=fakeca.test2"
openssl req -out test/certs/server_req2.pem -new -newkey rsa:4096 -nodes -keyout test/certs/server_key2.pem -subj "/C=US/ST=WA/L=Seattle/O=FakeTestingOrg/CN=localhost"
openssl x509 -req -days 365 -passin pass:fakepassword -in test/certs/server_req2.pem -CA test/certs/cacert2.pem -CAkey test/certs/cakey2.pem -out test/certs/server-cert2.pem -CAcreateserial -extfile <(printf "[SAN]\nsubjectAltName=DNS:localhost") -extensions SAN
