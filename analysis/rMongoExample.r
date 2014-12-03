
# Josh Willis
# November 2014
# willis2342@gmail.com
# 
# Use of rmongodb, a MongoDB library for R

library(rmongodb)

# ssh -L27017:da0.eecs.utk.edu:27017 -p 2200 -fN jwill221@da2.eecs.utk.edu 

# http://www.joyofdata.de/blog/mongodb-state-of-the-r-rmongodb/
# https://docs.compose.io/languages/r.html

host <- "localhost"
db <- "MapMyFitness"

mongo <- mongo.create(host=host , db=db)

workouts <- "workouts"
# http://www.statmethods.net/management/functions.html
namespace <- paste(db, workouts, sep=".") # MapMyFitness.workouts

# mongo.count(mongo, namespace, mongo.bson.empty())

json <- '{}'
bson <- mongo.bson.from.JSON(json)
cursor <- mongo.find(mongo, namespace, bson)
while(mongo.cursor.next(cursor)) {
  value <- mongo.cursor.value(cursor)
  list <- mongo.bson.to.list(value)
  str(list)
  break
}

