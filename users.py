
from fitness_api import *
from fitness_db import *

# Chris
CLIENT_ID = '3n3hce6yq6kz2r2h9mgbqc85rwy5r8qp'
CLIENT_SECRET = '2kkHbMQVvsEPXSk98VE3Cyd5cHMEYqzyHq82rutHe9A'

# Local computer connection using the following ssh command
# ssh -L27017:da0.eecs.utk.edu:27017 -p 2200 -fN jwill221@da2.eecs.utk.edu
host_name = 'localhost'

# UTK computer connection using the following ssh command
# ssh -p2200 jwill221@da2.eecs.utk.edu
# host_name = 'da0.eecs.utk.edu'

api = FitnessApi( CLIENT_ID, CLIENT_SECRET )
fitDb = FitnessDatabase( host_name )

while not fitDb.users_to_add_empty():

  user_to_add_doc = fitDb.get_user_to_add()
  userId = user_to_add_doc['userId']

  # Get docs via MapMyApi
  user_doc = api.get_user_doc( userId )
  friends_with_doc = api.get_friends_with_doc( userId )

  # Add users to database
  fitDb.users_insert( user_doc )
  fitDb.friends_with_insert( friends_with_doc )
  for user_doc in friends_with_doc['friends']:
    fitDb.users_to_add_insert( user_doc )

  fitDb.users_to_add_remove( user_to_add_doc )
