import pymongo
import threading
import thread
import time
import sys
from fitness_api import *
from fitness_db import *

def thread_proc(lock, client_id, client_secret, thread_id, user_array):
	
	#host_name = 'localhost'
	host_name = 'da0.eecs.utk.edu'

	api = FitnessApi( client_id, client_secret )
	fitDb = FitnessDatabase( host_name )

	while not fitDb.users_to_add_empty():

		lock.acquire()
		user_to_add_doc = fitDb.get_unique_user_to_add( thread_id, user_array )
		lock.release()
		userId = user_to_add_doc['userId']

		# Get docs via MapMyApi
		user_doc = api.get_user_doc( userId )
		if( user_doc == '' ):
			print 'Received empty string for user doc, continuing'
			continue
		# else:
			# friends_with_doc = api.get_friends_with_doc( userId )
        
		# if( friends_with_doc == '' ):
			# print 'Received empty string for friends_with_doc, continuing'
			# continue

		# Add users to database
		fitDb.users_insert( user_doc )
		# fitDb.friends_with_insert( friends_with_doc )
		# for user_doc in friends_with_doc['friends']:
			# fitDb.users_to_add_insert( user_doc )

		fitDb.users_to_add_remove( user_to_add_doc )

		sys.stdout.flush()
		sys.stderr.flush()


lock = threading.Lock()
CHRIS_ID = '3n3hce6yq6kz2r2h9mgbqc85rwy5r8qp'
CHRIS_SECRET = '2kkHbMQVvsEPXSk98VE3Cyd5cHMEYqzyHq82rutHe9A'

CAMILLE_ID = '2umhecdk2r3hxzvwuy2rx5x4rjeb427x'
CAMILLE_SECRET = 'fDsRmHDRmuAYUmqCHzRu4pqTrfNSDUfzk3BEK8c9cph'

JOSH_ID = 'jjd8nkcx3sjr6weurtjqun4hp6b5p7vk'
JOSH_SECRET = 'NNHSen7PqBXvyFneKvq4DvDetng6dU8kKZe8pYbx8E9'

DAVID_ID = 'cv8rzqn82xq9uub7ybta4y69jxfyfmjb'
DAVID_SECRET = 'WMbJFvksTUMgHFDTaCNtA9CRHmc8P6RhSUvXtF6cfny'

AUDRIS_ID = 'smyfv7ec67q7t6jqcfwhrv299x4g4rtv'
AUDRIS_SECRET = 'YGQEzsq877fhjZEEHR79F87EwjCn4ABncYTdvVfQGU8'

JOHN_ID = 'cx64t5vm27e2pzgwqaqvs2fsxhsrhd73'
JOHN_SECRET = 'yut7ya9PpYUkeDTtgRcdCH87Ee4eMXGXA5MK32GtWx5'

RJ_ID = 'njsuxksdpaxjg9rhs6hxjnjvusda57fp'
RJ_SECRET = 'yNrWJMaHF6pam9wj4TEpJcEuGE6dZ49Q3UujBhfRFD3'

ERIC_ID = '4frhp5dwf7jnze6dhxdj39ujhdbkygft'
ERIC_SECRET = 'DCceK33p3pc5YhpgYTBxGqFaax6ENHufsb4pKPMksj7'

#ofile_stdout = open('stdout.txt', 'w')
#ofile_stderr = open('stderr.txt', 'w')

#os.dup2(ofile_stdout.fileno(), sys.stdout.fileno())
#os.dup2(ofile_stderr.fileno(), sys.stderr.fileno())

IDs = [0,0,0,0,0,0,0,0]

t1 = threading.Thread(target=thread_proc, args=(lock, CHRIS_ID, CHRIS_SECRET, 0, IDs))
t1.start()
t2 = threading.Thread(target=thread_proc, args=(lock, CAMILLE_ID, CAMILLE_SECRET, 1, IDs))
t2.start()
t3 = threading.Thread(target=thread_proc, args=(lock, JOSH_ID, JOSH_SECRET, 2, IDs))
t3.start()
t4 = threading.Thread(target=thread_proc, args=(lock, DAVID_ID, DAVID_SECRET, 3, IDs))
t4.start()
t5 = threading.Thread(target=thread_proc, args=(lock, AUDRIS_ID, AUDRIS_SECRET, 4, IDs))
t5.start()
t6 = threading.Thread(target=thread_proc, args=(lock, JOHN_ID, JOHN_SECRET, 5, IDs))
t6.start()
t7 = threading.Thread(target=thread_proc, args=(lock, RJ_ID, RJ_SECRET, 6, IDs))
t7.start()
t8 = threading.Thread(target=thread_proc, args=(lock, ERIC_ID, ERIC_SECRET, 7, IDs))
t8.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()

print 'Done with master thread'
