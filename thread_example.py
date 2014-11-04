import pymongo
import threading
import thread
import time

def thread_proc(lock, client_id, client_secret, thread_id, user_array):
	client = pymongo.MongoClient('localhost')
	db = client['MapMyFitness']
	uta = db['users_to_add']
	print 'In thread' + str(thread_id) + '\n'
	lock.acquire()
	print 'Thread ' + str(thread_id) + ' got the lock'
	if(thread_id == 0):
		user = uta.find_one( { '$and': [ { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } } ] } )
	elif(thread_id == 1):
		user = uta.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[2] } }, { 'userId': { '$ne': user_array[3] } } ] } )
	elif(thread_id == 2):
		user = uta.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[3] } } ] } )
	elif(thread_id == 3):
		user = uta.find_one( { '$and': [ { 'userId': { '$ne': user_array[0] } }, { 'userId': { '$ne': user_array[1] } }, { 'userId': { '$ne': user_array[2] } } ] } )
	print user
	user_array[thread_id] = user['userId']
	print 'Current array:'
	print user_array
	lock.release()

	# do normal stuff here

	exit()


lock = threading.Lock()

names = ['','','','']
thread_counter = 0

for i in range(4):
	t = threading.Thread(target=thread_proc, args=(lock, '0', '0', thread_counter, names))
	t.start()
	# print 'Created thread ' + str(thread_counter)
	thread_counter += 1

print 'Done with master thread'