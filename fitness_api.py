
import requests
from datetime import datetime, date, time, timedelta

class FitnessApi:
  def __init__(self, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret

    self.calls = 0
    self.limit = 24500

    self.access_token = self.get_access_token()

  def increment_calls( self ):
    self.calls += 1
    if self.calls > self.limit:
      print 'Reached API call limit. Waiting until next refresh time.'
      self.wait()

      print 'Refreshed. Grabbing more users.'
      self.calls = 0
    return

  def request( self, request_url ):
    response = requests.get(url=request_url, verify=False, headers={
                'api-key': self.client_id, 'authorization': 'Bearer %s' % self.access_token['access_token']})
    self.increment_calls()

    return response.json()

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

    response = requests.post(url=access_token_url, data=access_token_data,
                headers={'Api-Key': self.client_id})
    self.increment_calls()

    try:
      access_token = response.json()
    except:
      print 'Did not get JSON. Here is the response and content:'
      print response 
      print response.content 

    return access_token

  

  def wait( self ):
    # Refresh at 12:30 AM GMT the next day
    next_day = timedelta(days=1)
    next_refresh_date = now.date() + next_day
    next_refresh_time = time(0, 30)
    next_refresh = datetime.combine( next_refresh_date, next_refresh_time )

    # Wait until the next refresh period
    while datetime.utcnow() < next_refresh:
      continue

    return
  

