
import pymongo
from bson import json_util

verbose = False

client = pymongo.MongoClient('localhost')
fitnessDb = client['MapMyFitness']

users = fitnessDb['users']
users_to_add = fitnessDb['users_to_add']
friends_with = fitnessDb['friends_with']

print '# users: ' + str(users.count())
print '# users to add: ' + str(users_to_add.count())
print '# users with friends: ' + str(friends_with.count())

if verbose:
	for user in users.find():
		print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

	for user in users_to_add.find():
		print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

	for user in friends_with.find():
		print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

# users.remove()
# users_to_add.remove()
# friends_with.remove()
