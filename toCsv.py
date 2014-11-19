

import pymongo
import codecs

# ssh -L27017:da0.eecs.utk.edu:27017 -p 2200 -fN jwill221@da2.eecs.utk.edu

def get_headers( doc ):
  # Get headers
  s = ''
  workout = doc['workout']
  for field in workout:

    if field == '_links' or field == 'notes' or field == 'name':
      continue

    if field == 'aggregates':
      for field in workout[field]:
        s += str( field ) + ','
    else:
      s += str( field ) + ','

  s += 'userId\n'
  return s

def get_values( doc ):
  s = ''
  workout = doc['workout']
  for field in workout:

    if field == '_links' or field == 'notes' or field == 'name':
      continue

    if field == 'aggregates':
      aggregates = workout[field]
      for aggregate in aggregates:
        try:
          value = str( aggregates[aggregate] )
        except:
          value = ''
        s += value + ','
    else:
      try:
        value = str( workout[field] )
      except:
        value = ''
      s += value + ','

  s += str( doc['userId'] ) + '\n'
  return s

client = pymongo.MongoClient('localhost')
# client = pymongo.MongoClient('da0.eecs.utk.edu')
db = client['MapMyFitness']
workouts = db['workouts']

# doc = workouts.find_one()
# doc = workouts.find(fields={ '_id' : 0 })[40]
# doc = workouts.find(fields={ '_id' : 0 })[463876]

# f = open('workouts.csv', 'w')
# headers = get_headers( doc )
# values = get_values( doc )
# f.write( headers )
# f.write( values )
# f.close()

f = open('workouts.csv', 'w')
for doc in workouts.find():
  headers = get_headers( doc )
  values = get_values( doc )
  f.write( headers )
  f.write( values )
f.close()


