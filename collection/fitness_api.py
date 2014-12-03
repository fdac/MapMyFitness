# Chris Daffron and Josh Willis
# willis2342@gmail.com
# November 2014

import requests
import time as time2
import math
import thread
from datetime import datetime, date, time, timedelta
import sys

import urlparse
import webbrowser
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json

# Set up a basic handler for the redirect issued by the mapmyfitness
# authorize page. For any GET request, it simply returns a 200.
# When run interactively, the request's URL will be printed out

class AuthorizationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.server.path = self.path

class FitnessApi:
  def __init__(self, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret

    self.calls = 0
    self.calls_second = 0
    self.last_time = time2.time()
    self.limit = 24500
    self.sec_limit = 55

    try:
      with open('access_token_' + client_id, 'r') as f:
        self.access_token = json.load( f )
    except:
      self.access_token = self.get_authorization_access_token()
      with open('access_token_' + client_id, 'w') as f:
        json.dump( self.access_token, f, sort_keys=False, indent=2, separators=(',',':') )


  def increment_calls( self ):
    self.calls += 1
    self.calls_second += 1

    # If over daily API call limit
    if self.calls > self.limit:
      print 'Reached API call limit. Waiting until next refresh time.'
      self.wait()

      print 'Refreshed. Grabbing more users.'
      self.calls = 0
      self.calls_second = 0

    # If over seconds API call limit
    elif self.calls_second > self.sec_limit:
      print 'Reached API calls/sec limit. Waiting until next second.'
      self.sec_wait()

      print 'Refreshed. Grabbing more users.'
      # self.calls = 0
      self.calls_second = 0
    elif time2.time >= self.last_time + 1:
      self.last_time = time2.time()
      self.calls_second = 0
    return

  def request( self, request_url ):
    try:
      response = requests.get(url=request_url, verify=False, headers={
                  'api-key': self.client_id, 'authorization': 'Bearer %s' % self.access_token['access_token']})
    except:
      print 'API request failed (not error code)'
      return ''

    headers = response.headers
    try:
      callsPerSecond = int( headers['X-Plan-Qps-Current'] )
      callsPerDay = int( headers['X-Plan-Quota-Current'] )

      if callsPerSecond >= 60:
        next_sec = time2.time() + 1
        while time2.time() < next_sec:
          time2.sleep( abs(next_sec - time2.time()) )

      if callsPerDay >= self.limit:
        self.wait()

    except:
      print 'You stoop'
      print headers
      sys.exit()

    #print response.content

    # Over API call limit
    #if( response.status_code == 403 ):
    #  self.calls = self.limit

    # self.increment_calls()

    # Print debug info if the call fails
    if( response.status_code != 200 ):
      print 'ERROR! Received a status code of ' + str(response.status_code) + '\n'
      print 'URL: ' + str(request_url) + '\n'
      print 'Received Content:'
      print response.content

    try:
      return response.json()
    except:
      return ''

  def get_user_doc( self, userId ):
    request_url = 'https://oauth2-api.mapmyapi.com/v7.0/user/' + str(userId) + '/'
    user_doc = self.request(request_url)
    return user_doc

  def get_friends_with_doc( self, userId ): 
    friends_with_doc = { 'userId' : userId, 'friends' : [] }

    next_url = 'https://oauth2-api.mapmyapi.com/v7.0/user/?limit=20&friends_with=' + str( userId ) + '&offset=0'
    while next_url:
      friends_with_response = self.request( next_url )
      
      friends = friends_with_response['_embedded']['user']
      for friend in friends:
        user = { 'userId' : friend['id'] }
        friends_with_doc['friends'].append( user )

      try:
	next_url = 'https://oauth2-api.mapmyapi.com' + friends_with_response['_links']['next'][0]['href']
      except:
        next_url = ''

    return friends_with_doc

  def get_workouts_docs( self, userId ):

    workouts_doc = { 'userId' : userId, 'workout' : {} }
    workouts_docs = []
    next_url = 'https://oauth2-api.mapmyapi.com/v7.0/workout/?user=%2Fv7.0%2Fuser%2F' + str(userId) + '%2F'
    while next_url:
      print 'ID: ' + str(userId) + ' workout page'
      workouts_response = self.request( next_url )
      workouts = workouts_response['_embedded']['workouts']
      for workout in workouts:
    	workouts_doc = { 'userId' : userId, 'workout' : workout }
        #workouts_doc['workout'] = workout
        workouts_docs.append( workouts_doc )

      try:
        next_url = 'https://oauth2-api.mapmyapi.com' + workouts_response['_links']['next'][0]['href']
	print 'Found next URL'
      except:
        next_url = ''
        print 'Did not find next URL'

    print 'Returning workouts doc'
    return workouts_docs

  def get_client_access_token( self ):
    access_token_url = 'https://api.mapmyfitness.com/v7.0/oauth2/access_token/'
    access_token_data = {'grant_type': 'client_credentials',
              'client_id': self.client_id,
              'client_secret': self.client_secret}
    try:
      response = requests.post(url=access_token_url, data=access_token_data,
                  headers={'Api-Key': self.client_id})
    except:
      print 'Request for access token failed (not error code)'
      thread.exit()
      
    self.increment_calls()

    # Print out debug info if the call is not successful
    if( response.status_code != 200 ):
      print 'ERROR! Received a status code of ' + str(response.status_code) + '\n'
      print 'URL: ' + str(access_token_url) + '\n'
      print 'Data: ' + str(access_token_data) + '\n'
      print 'Received Content:'
      print response.content
      thread.exit()

    try:
      access_token = response.json()
    except:
      print 'Did not get JSON. Here is the response and content:'
      print response 
      print response.content 
      access_token = ''

    return access_token

  def get_authorization_access_token(self):
    # As a convenience, localhost.mapmyapi.com redirects to localhost.
    redirect_uri = 'http://localhost.mapmyapi.com:12345/callback'
    authorize_url = 'https://www.mapmyfitness.com/v7.0/oauth2/authorize/?' \
                    'client_id={0}&response_type=code&redirect_uri={1}'.format(self.client_id, redirect_uri)

    parsed_redirect_uri = urlparse.urlparse(redirect_uri)
    server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

    # NOTE: Don't go to the web browser just yet...
    webbrowser.open(authorize_url)

    # Start our web server, handle_request() will block until a request comes in.
    httpd = HTTPServer(server_address, AuthorizationHandler)
    httpd.handle_request()

    # At this point a request has been handled. Let's parse its URL.
    httpd.server_close()
    callback_url = urlparse.urlparse(httpd.path)
    authorize_code = urlparse.parse_qs(callback_url.query)['code'][0]

    access_token_url = 'https://api.mapmyfitness.com/v7.0/oauth2/access_token/'
    access_token_data = {'grant_type': 'authorization_code',
                         'client_id': self.client_id,
                         'client_secret': self.client_secret,
                         'code': authorize_code}

    response = requests.post(url=access_token_url,
                             data=access_token_data,
                             headers={'Api-Key': self.client_id})

    try:
        access_token = response.json()
        print 'Got an access token:', access_token
    except:
        print 'Did not get JSON. Here is the response and content:'
        print response
        print response.content

    return access_token

  def wait( self ):
    # Refresh at 12:30 AM GMT the next day
    now = datetime.utcnow()
    next_day = timedelta(days=1)
    next_refresh_date = now.date() + next_day
    next_refresh_time = time(0, 30)
    next_refresh = datetime.combine( next_refresh_date, next_refresh_time )

    # Wait until the next refresh period
    while datetime.utcnow() < next_refresh:
      difference = next_refresh - datetime.utcnow()
      time2.sleep(difference.total_seconds())

    return
  
  def sec_wait(self):
    # Wait until the next second
    next_sec = self.last_time + 1
    while time2.time() < next_sec:
      time2.sleep( abs(next_sec - time2.time()))

    self.last_time = time2.time()

    return

