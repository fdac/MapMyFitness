
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

  if count > 2:
    # Remove first instance
    # users.remove( { '_id' : cursor[0]['_id'] } ) 
  

f.close()

