import pymongo
import threading
import thread
import time
import sys
from fitness_api import *
# from fitness_db import *

MMFapi = FitnessApi('7', '7')
for i in range(10):
    print 'Start getting user doc'
    sys.stdout.flush()
    MMFapi.get_user_doc(5)
    print 'Done getting user doc'
    sys.stdout.flush()