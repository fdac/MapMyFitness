import logging
import urlparse
import requests
import json

# logging.basicConfig(level=logging.DEBUG)
CLIENT_ID = '3n3hce6yq6kz2r2h9mgbqc85rwy5r8qp'
CLIENT_SECRET = '2kkHbMQVvsEPXSk98VE3Cyd5cHMEYqzyHq82rutHe9A'

def get_access_token():

    # As a convenience, localhost.mapmyapi.com redirects to localhost.
    redirect_uri = 'http://localhost.mapmyapi.com:12345/callback'
    authorize_url = 'https://www.mapmyfitness.com/v7.0/oauth2/authorize/?' \
                    'client_id={0}&response_type=code&redirect_uri={1}'.format(CLIENT_ID, redirect_uri)

    parsed_redirect_uri = urlparse.urlparse(redirect_uri)
    server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

    access_token_url = 'https://api.mapmyfitness.com/v7.0/oauth2/access_token/'
    access_token_data = {'grant_type': 'client_credentials',
                         'client_id': CLIENT_ID,
                         'client_secret': CLIENT_SECRET}

    response = requests.post(url=access_token_url,
                             data=access_token_data,
                             headers={'Api-Key': CLIENT_ID})

    # retrieve the access_token from the response
    try:
        access_token = response.json()
        # print 'Got an access token:', access_token
    except:
        print 'Did not get JSON. Here is the response and content:'
        print response
        print response.content

    return access_token

def api_request(request_url, access_token):
    response = requests.get(url=request_url, verify=False,
                            headers={'api-key': CLIENT_ID, 'authorization': 'Bearer %s' % access_token['access_token']})

    return response.json()



