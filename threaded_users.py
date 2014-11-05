import pymongo
import threading
import thread
import time
from fitness_api import *
from fitness_db import *

def thread_proc(lock, client_id, client_secret, thread_id, user_array):
	
	host_name = 'localhost'

	api = FitnessApi( client_id, client_secret )
	fitDb = FitnessDatabase( host_name )

	while not fitDb.users_to_add_empty():

		lock.acquire()
		user_to_add_doc = fitDb.get_unique_user_to_add( thread_id, user_array )
		lock.release()
		userId = user_to_add_doc['userId']

		# Get docs via MapMyApi
		user_doc = api.get_user_doc( userId )
		friends_with_doc = api.get_friends_with_doc( userId )

		# Add users to database
		fitDb.users_insert( user_doc )
		fitDb.friends_with_insert( friends_with_doc )
		for user_doc in friends_with_doc['friends']:
			fitDb.users_to_add_insert( user_doc )

		fitDb.users_to_add_remove( user_to_add_doc )


lock = threading.Lock()
CHRIS_ID = '3n3hce6yq6kz2r2h9mgbqc85rwy5r8qp'
CHRIS_SECRET = '2kkHbMQVvsEPXSk98VE3Cyd5cHMEYqzyHq82rutHe9A'

CAMILLE_ID = '2umhecdk2r3hxzvwuy2rx5x4rjeb427x'
CAMILLE_SECRET = 'fDsRmHDRmuAYUmqCHzRu4pqTrfNSDUfzk3BEK8c9cph'

JOSH_ID = 'jjd8nkcx3sjr6weurtjqun4hp6b5p7vk'
JOSH_SECRET = 'NNHSen7PqBXvyFneKvq4DvDetng6dU8kKZe8pYbx8E9'

IDs = [0,0,0]

t = threading.Thread(target=thread_proc, args=(lock, CHRIS_ID, CHRIS_SECRET, 0, IDs))
t.start()
t = threading.Thread(target=thread_proc, args=(lock, CAMILLE_ID, CAMILLE_SECRET, 1, IDs))
t.start()
t = threading.Thread(target=thread_proc, args=(lock, JOSH_ID, JOSH_SECRET, 2, IDs))
t.start()

print 'Done with master thread'