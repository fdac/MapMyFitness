
import pymongo

client = pymongo.MongoClient('da0.eecs.utk.edu')
db = client['MapMyFitness']
users = db['users']

duplicates = { }

index = 0
length = users.count()
listOfUsers = users.find()

f = open('duplicates.txt', 'w')

for index in range(index, length):
  user = listOfUsers[index]
  userId = user['id']
 
  print 'Index: ' + str( index ) 
  if duplicates.get( userId ) != None:
    duplicates[ userId ] += 1
    f.write( str(userId) + "\n" )
  else:
    duplicates[ userId ] = 1
  

f.close()

