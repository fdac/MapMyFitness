
import requests
import time as time2
import math
from datetime import datetime, date, time, timedelta

class FitnessApi:
  def __init__(self, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret

    self.calls = 0
    self.calls_second = 0
    self.last_time = time2.time()
    self.limit = 24500
    self.sec_limit = 55

    self.access_token = self.get_access_token()

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
      self.calls = 0
    return

  def request( self, request_url ):
    try:
      response = requests.get(url=request_url, verify=False, headers={
                  'api-key': self.client_id, 'authorization': 'Bearer %s' % self.access_token['access_token']})
    except:
      print 'API request failed (not error code)'
      return ''
    
    # Over API call limit
    #if( response.status_code == 403 ):
    #  self.calls = self.limit

    self.increment_calls()

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
    request_url = 'https://oauth2-api.mapmyapi.com/v7.0/user/' + str(userId)
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
        next_url = friends_with_response['_links']['next']['href']
      except:
        next_url = ''

    return friends_with_doc

  def get_access_token( self ):
    access_token_url = 'https://api.mapmyfitness.com/v7.0/oauth2/access_token/'
    access_token_data = {'grant_type': 'client_credentials',
              'client_id': self.client_id,
              'client_secret': self.client_secret}
    try:
      response = requests.post(url=access_token_url, data=access_token_data,
                  headers={'Api-Key': self.client_id})
    except:
      print 'Request for access token failed (not error code)'
      exit()
      
    self.increment_calls()

    # Print out debug info if the call is not successful
    if( response.status_code != 200 ):
      print 'ERROR! Received a status code of ' + str(response.status_code) + '\n'
      print 'URL: ' + str(access_token_url) + '\n'
      print 'Data: ' + str(access_token_data) + '\n'
      print 'Received Content:'
      print response.content

    try:
      access_token = response.json()
    except:
      print 'Did not get JSON. Here is the response and content:'
      print response 
      print response.content 
      access_token = ''

    return access_token

  

  def wait( self ):
    # Refresh at 12:30 AM GMT the next day
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
      time2.sleep( math.abs(next_sec - time2.time()))

    self.last_time = time2.time()

    return

