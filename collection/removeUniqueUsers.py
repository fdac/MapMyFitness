# Chris Daffron and Josh Willis
# willis2342@gmail.com
# November 2014

import pymongo

client = pymongo.MongoClient('da0.eecs.utk.edu')
db = client['MapMyFitness']
users = db['users']

f = open('duplicates.txt', 'r')

for userId in f:
  userId = userId.replace('\n', '')
  
  cursor = users.find( { 'id' : int( userId ) } )
  count = cursor.count()
  print str( userId ) + ": " + str( count )

  if count >= 2:
    # Remove first instance
    for i in range(count-1):
        users.remove( { '_id' : cursor[i]['_id'] } ) 
  

f.close()

