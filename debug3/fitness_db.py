
import pymongo


class FitnessDatabase:

  def __init__(self, host_name):
    self.client = pymongo.MongoClient(host_name)
    self.fitnessDb = self.client['MapMyFitness']

    self.users = self.fitnessDb['users']
    self.users_to_add = self.fitnessDb['users_copy2']
    self.friends_with = self.fitnessDb['friends_with']
    self.workouts = self.fitnessDb['workouts']

  def get_workouts_collection(self):
    return self.workouts

  def get_users_collection(self):
    return self.users_to_add

  def users_insert(self, user_doc):
    userId = user_doc['id']
    ret = self.users.find_one({'id': userId})
    not_already_added = (ret == None)

    if not_already_added:
      print 'Adding ' + str(userId) + ' to users'

      try:
        self.users.insert(user_doc)
      except:
        print 'Error: Unable to add ' + str(userId) + ' to users'

    else:
      print 'Not adding ' + str(userId) + ' to users'

  def friends_with_insert(self, friends_with_doc):
    userId = friends_with_doc['userId']
    ret = self.friends_with.find_one({'userId': userId})
    not_already_added = (ret == None)

    if not_already_added:
      print 'Adding ' + str(userId) + ' to friends_with'

      try:
        self.friends_with.insert(friends_with_doc)
      except:
        print 'Error: Unable to add ' + str(userId) + ' to friends_with'

    else:
      print 'Not adding ' + str(userId) + ' to friends_with'

  def users_to_add_insert(self, user_doc):
    userId = user_doc['userId']
    ret1 = self.users.find_one({'id': userId})
    ret2 = self.users_to_add.find_one({'userId': userId})

    not_already_added = (ret1 == None) and (ret2 == None)
    if not_already_added:
      print 'Adding ' + str(userId) + ' to users_to_add'

      try:
        self.users_to_add.insert(user_doc)
      except:
        print 'Error: Unable to add ' + str(userId) + ' to users_to_add'

    else:
      print 'Not adding ' + str(userId) + ' to users_to_add'

  def users_to_add_remove(self, user_doc):
    self.users_to_add.remove(user_doc)

  def get_num_users_to_add(self):
    return self.users_to_add.count()

  def users_to_add_empty(self):
    if self.get_num_users_to_add() == 0:
      return True
    return False

  def get_user_to_add(self):
    return self.users_to_add.find_one()

  def get_user(self):
    return self.users.find_one()

  def get_unique_user_to_add(self, thread_id, user_array):
    if( thread_id == 0    ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
      return self.users_to_add.find_one( { '$and': [ { 'id': { '$ne': user_array[1] } }, { 'id': { '$ne': user_array[2] } }, { 'id': { '$ne': user_array[3] } }, { 'id': { '$ne': user_array[4] } }, { 'id': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } } ] } )
    elif( thread_id == 1  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
      return self.users_to_add.find_one( { '$and': [ { 'id': { '$ne': user_array[0] } }, { 'id': { '$ne': user_array[2] } }, { 'id': { '$ne': user_array[3] } }, { 'id': { '$ne': user_array[4] } }, { 'id': { '$ne': user_array[5] } }, { 'id': { '$ne': user_array[6] } } ] } )
    elif( thread_id == 2  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
      return self.users_to_add.find_one( { '$and': [ { 'id': { '$ne': user_array[0] } }, { 'id': { '$ne': user_array[1] } }, { 'id': { '$ne': user_array[3] } }, { 'id': { '$ne': user_array[4] } }, { 'id': { '$ne': user_array[5] } }, { 'id': { '$ne': user_array[6] } } ] } )
    elif( thread_id == 3  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
      return self.users_to_add.find_one( { '$and': [ { 'id': { '$ne': user_array[0] } }, { 'id': { '$ne': user_array[1] } }, { 'id': { '$ne': user_array[2] } }, { 'id': { '$ne': user_array[4] } }, { 'id': { '$ne': user_array[5] } }, { 'id': { '$ne': user_array[6] } } ] } )
    elif( thread_id == 4  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
      return self.users_to_add.find_one( { '$and': [ { 'id': { '$ne': user_array[0] } }, { 'id': { '$ne': user_array[1] } }, { 'id': { '$ne': user_array[2] } }, { 'id': { '$ne': user_array[3] } }, { 'id': { '$ne': user_array[5] } }, { 'id': { '$ne': user_array[6] } } ] } )
    elif( thread_id == 5  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
      return self.users_to_add.find_one( { '$and': [ { 'id': { '$ne': user_array[0] } }, { 'id': { '$ne': user_array[1] } }, { 'id': { '$ne': user_array[2] } }, { 'id': { '$ne': user_array[3] } }, { 'id': { '$ne': user_array[4] } }, { 'id': { '$ne': user_array[6] } } ] } )
    elif( thread_id == 6  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
      return self.users_to_add.find_one( { '$and': [ { 'id': { '$ne': user_array[0] } }, { 'id': { '$ne': user_array[1] } }, { 'id': { '$ne': user_array[2] } }, { 'id': { '$ne': user_array[3] } }, { 'id': { '$ne': user_array[4] } }, { 'id': { '$ne': user_array[5] } } ] } )
    # elif( thread_id == 7  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    # elif( thread_id == 8  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    # elif( thread_id == 9  ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    # elif( thread_id == 10 ):
      # return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9]  } } ] } )

  def get_userIds(self, thread_id, num_threads):
    ret = []

    index = thread_id
    count = self.users.count()
    step = num_threads

    # findResults = self.users.find()

    for index in range(index, count, step):

      print 'Index: ' + str(index)
      print 'User ID: ' + str( findResults[index]['id'] )
      
      user = findResults[index]
      userId = user['id']

      # Workout request
      # Add to the workouts collection

      # ret.append( userId )

    print 'Got userIds for thread ' + thread_id

  def workouts_insert(self, workouts_docs):
    self.workouts.insert(workouts_docs)

    # userId = workouts_doc['id']
    # ret = self.workouts.find_one({'userId': userId})
    # not_already_added = (ret == None)

    # if not_already_added:
    #   print 'Adding ' + str(userId) + ' to workouts'

    #   try:
    #     self.workouts.insert(user_doc)
    #   except:
    #     print 'Error: Unable to add ' + str(userId) + ' to workouts'

    # else:
    #   print 'Not adding ' + str(userId) + ' to workouts'

