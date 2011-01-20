#!/usr/bin/env python
# -*- coding: utf-8 -*-

# command line script to create a token

# Use this to create a token
# after: ./manage.py syncdb     # reply no to admin user as admin/foobar is available in the fixtures
# and:   ./manage.py runserver  # in a second terminal
# run:   ./oauth_client.py      # cut and paster the URL into a new browser instance
# in the browser login with testuser/foobar   (or admin/foobar)
# check the checkbox and submit the form
# paste the PIN value to this script and confirm
# then there will be a Token in the database
# run the proxy command in a third terminal
#   - may need to be in oauth_proxy directory to run
#   - get from: git clone git://github.com/mojodna/oauth-proxy.git
# run the two curl commands and see the JSON responses
# in the browser inspect the root URL to see the new entries

# if this script is failing open log*.html in a browser to see the Django stack trace

import os
import cgi
import oauth2 as oauth

# settings for the local test consumer
CONSUMER_SERVER = os.environ.get("CONSUMER_SERVER") or 'localhost'
CONSUMER_PORT = os.environ.get("CONSUMER_PORT") or '8000'
print 'Server = ', CONSUMER_SERVER, CONSUMER_PORT

# for the oauth_proxy example below
PROXY_PORT = os.environ.get("PROXY_PORT") or '8001'

# fake urls for the test server (matches ones in server.py)
REQUEST_TOKEN_URL = 'http://{host:s}:{port:s}/api/oauth/request_token/'.format(host=CONSUMER_SERVER, port=CONSUMER_PORT)
ACCESS_TOKEN_URL = 'http://{host:s}:{port:s}/api/oauth/access_token/'.format(host=CONSUMER_SERVER, port=CONSUMER_PORT)
AUTHORIZE_URL = 'http://{host:s}:{port:s}/api/oauth/authorize/'.format(host=CONSUMER_SERVER, port=CONSUMER_PORT)

# key and secret granted by the service provider for this consumer application - same as the MockOAuthDataStore
CONSUMER_KEY = 'testkey'
CONSUMER_SECRET = 'testsecret'


consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth.Client(consumer)

# Step 1: Get a request token. This is a temporary token that is used for
# having the user authorize an access token and to sign the request to obtain
# said access token.

resp, content = client.request(REQUEST_TOKEN_URL, "GET")
if resp['status'] != '200':
    with open('log1.html', 'w') as f:
        f.write(content)
    raise Exception("Invalid response {r:s}".format(r=resp['status']))

request_token = dict(cgi.parse_qsl(content))

print "Request Token:"
print "    - oauth_token        = {token:s}".format(token=request_token['oauth_token'])
print "    - oauth_token_secret = {secret:s}".format(secret=request_token['oauth_token_secret'])
print

# Step 2: Redirect to the provider. Since this is a CLI script we do not
# redirect. In a web application you would redirect the user to the URL
# below.

print "Go to the following link in your browser:"
print
print "{url:s}?oauth_token={token:s}".format(url=AUTHORIZE_URL, token=request_token['oauth_token'])
print
print "Check the Authorize access box and press Confirm"
print "then copy the displayed PIN and paste into the prompt below"
print

# After the user has granted access to you, the consumer, the provider will
# redirect you to whatever URL you have told them to redirect to. You can
# usually define this in the oauth_callback argument as well.
accepted = 'n'
while accepted.lower() != 'y':
    oauth_verifier = raw_input('Enter the PIN from browser: ')
    print 'PIN = {pin:s}'.format(pin=oauth_verifier)
    accepted = raw_input('Confirm PIN was copied correctly [y/n] ? ')

# Step 3: Once the consumer has redirected the user back to the oauth_callback
# URL you can request the access token the user has approved. You use the
# request token to sign this request. After this is done you throw away the
# request token and use the access token returned. You should store this
# access token somewhere safe, like a database, for future use.
token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp, content = client.request(ACCESS_TOKEN_URL, "POST")
with open('log2.html', 'w') as f:
    f.write(content)
access_token = dict(cgi.parse_qsl(content))

print "Access Token:"
print "    - oauth_token        = {token:s}".format(token=access_token['oauth_token'])
print "    - oauth_token_secret = {secret:s}".format(secret=access_token['oauth_token_secret'])
print
print "You may now access protected resources using the access tokens above."
print

print 'example for use with oauth_proxy from: git://github.com/mojodna/oauth-proxy.git'
print
cmd = "twistd -n oauth_proxy --consumer-key '{ck:s}' --consumer-secret '{cs:s}' --token '{tk:s}' --token-secret '{ts:s}'"
print cmd.format(
    ck=CONSUMER_KEY, cs=CONSUMER_SECRET,
    tk=access_token['oauth_token'], ts=access_token['oauth_token_secret'])
print

print 'some curl examples to upload via the above proxy'
print
for t, c in (
    ('post one', 'content for post one'),
    ('post two', 'content for post two'),
    ):

    print "curl -x 'http://{host:s}:{proxy:s}' 'http://{host:s}:{port:s}/api/posts.json' -F 'title={t:s}' -F 'content={c:s}'".format(proxy=PROXY_PORT, host=CONSUMER_SERVER, port=CONSUMER_PORT, c=c, t=t)
