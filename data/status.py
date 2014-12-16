
# Get the # of users currently in each collection

import pymongo
from bson import json_util

verbose = False

# client = pymongo.MongoClient('localhost')
client = pymongo.MongoClient('da0.eecs.utk.edu')
fitnessDb = client['MapMyFitness']

users = fitnessDb['users']
users_to_add = fitnessDb['users_to_add']
users_to_add_copy2 = fitnessDb['users_to_add_copy2']
friends_with = fitnessDb['friends_with']

print '# users: ' + str(users.count())
print '# users to add: ' + str(users_to_add.count())
print '# users with friends: ' + str(friends_with.count())
print '# users to add copy2: ' + str(users_to_add_copy2.count())

if verbose:

  # Print a single example document from every collection
  user = users.find_one()
  print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

  user = users_to_add.find_one()
  print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

  user = friends_with.find_one()
  print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

  # Print all documents from every collection
  # for user in users.find():
  #   print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

  # for user in users_to_add.find():
  #   print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )

  # for user in friends_with.find():
  #   print json_util.dumps( user, sort_keys=False, indent=2, separators=( ',', ':' ) )




# DANGEROUS! REMOVES ALL ENTRIES IN EACH COLLECTION!
# users.remove()
# users_to_add.remove()
# friends_with.remove()
