
import pymongo


class FitnessDatabase:

  def __init__(self, host_name):
    self.client = pymongo.MongoClient(host_name)
    self.fitnessDb = self.client['MapMyFitness']

    self.users = self.fitnessDb['users']
    self.users_to_add = self.fitnessDb['users_to_add_copy2']
    self.friends_with = self.fitnessDb['friends_with']

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

  def get_unique_user_to_add(self, thread_id, user_array):
    if( thread_id == 0    ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 1  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 2  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 3  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 4  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 5  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 6  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 7  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 8  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[9] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 9  ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[10] } } ] } )
    elif( thread_id == 10 ):
      return self.users_to_add.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } }, { 'userId': { '$ne': user_array[4] } }, { 'userId': { '$ne': user_array[5] } }, { 'userId': { '$ne': user_array[6] } }, { 'userId': { '$ne': user_array[7] } }, { 'userId': { '$ne': user_array[8] } }, { 'userId': { '$ne': user_array[9]  } } ] } )

