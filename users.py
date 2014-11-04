
from fitness_request import *
import pymongo
import json

# MapMyFitness API Calls
def get_user_doc( userId ):
	request_url = 'https://oauth2-api.mapmyapi.com/v7.0/user/' + str(userId)
	user_doc = api_request(request_url, access_token)
	return user_doc

def get_friends_with_doc( userId ):
	friends_with_doc = { 'userId' : userId, 'friends' : [] }

	next_url = 'https://oauth2-api.mapmyapi.com/v7.0/user/?limit=20&friends_with=' + str(userId) + '&offset=0'
	while next_url:
		friends_with_response = api_request(next_url, access_token)
		
		friends = friends_with_response['_embedded']['user']
		for friend in friends:
			user = { 'userId' : friend['id'] }
			friends_with_doc['friends'].append( user )

		try:
			next_url = friends_with_response['_links']['next']['href']
		except:
			next_url = ''

	return friends_with_doc


# Database Entry Functions
def users_insert( users_collection, user_doc ):
	ret = users_collection.find_one( { 'id' : user_doc['id'] } )
	not_already_added = ( ret == None )
	
	if not_already_added:
		print 'Adding ' + str( user_doc['id'] ) + ' to users'

		try:
			users_collection.insert( user_doc )
		except:
			print 'Error: Unable to add ' + str( user_doc['id'] ) + ' to users'

	else:
		print 'Not adding ' + str( user_doc['id'] ) + ' to users'

def friends_with_insert( friends_with_collection, friends_with_doc ):
	ret = friends_with_collection.find_one( { 'userId' : friends_with_doc['userId'] } )
	not_already_added = ( ret == None )

	if not_already_added:
		print 'Adding ' + str( userId ) + ' to friends_with'

		try:
			friends_with_collection.insert( friends_with_doc )
		except:
			print 'Error: Unable to add ' + str( userId ) + ' to friends_with'

	else:
		print 'Not adding ' + str( userId ) + ' to friends_with'


def users_to_add_insert( users_collection, users_to_add_collection, user_doc ):
	ret1 = users.find_one( { 'id' : user_doc['userId'] } )
	ret2 = users_to_add.find_one( { 'userId' : user_doc['userId'] } )

	not_already_added = ( ret1 == None ) and ( ret2 == None )
	if not_already_added:
		print 'Adding ' + str( user_doc['userId'] ) + ' to users_to_add'

		try:
			users_to_add.insert( user_doc )
		except:
			print 'Error: Unable to add ' + str( user_doc['userId'] ) + ' to users_to_add'

	else:
		print 'Not adding ' + str( user_doc['userId'] ) + ' to users_to_add'





access_token_file = 'access_token'
try:
	with open(access_token_file, 'r') as f:
		access_token = json.loads(f)
except:
	access_token = get_access_token()
	with open(access_token_file, 'w') as f:
		json.dump(access_token, f)

# ssh -L27017:da0.eecs.utk.edu:27017 -p 2200 -fN jwill221@da2.eecs.utk.edu
# client = pymongo.MongoClient('localhost')
client = pymongo.MongoClient('da0.eecs.utk.edu')
fitnessDb = client['MapMyFitness']

users = fitnessDb['users']
users_to_add = fitnessDb['users_to_add']
friends_with = fitnessDb['friends_with']

# userId = 54889592
# user_doc = { 'userId' : userId }
# users_to_add_insert( users, users_to_add, user_doc )

while users_to_add.count() != 0:

	user_to_add_doc = users_to_add.find_one()
	userId = user_to_add_doc['userId']

	# Get docs via MapMyApi
	user_doc = get_user_doc( userId )
	friends_with_doc = get_friends_with_doc( userId )

	# Add users to database
	users_insert( users, user_doc )
	friends_with_insert( friends_with, friends_with_doc )
	for user_doc in friends_with_doc['friends']:
		users_to_add_insert( users, users_to_add, user_doc )

	users_to_add.remove( user_to_add_doc )

	# break
	


