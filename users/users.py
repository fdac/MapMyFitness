import pymongo
import threading
import thread
import time
import sys
from fitness_api import *
from fitness_db import *

def thread_proc (client_id, client_secret, thread_id, user_array):
  host_name = 'da0.eecs.utk.edu'
  fitDb = FitnessDatabase (host_name)
  api = FitnessApi (client_id, client_secret)
  print "starting" + client_id + ";" + client_secret
  for line in sys .stdin:
    userId = int(line .rstrip ())
    print "userID:" + str(userId)
    user_doc = api.get_user_doc (userId)
    if (user_doc == ''):
      print 'Received empty string for user doc, continuing' + str(userId)
      continue
    fitDb.users_insert (user_doc, True)
    sys.stdout.flush()
    sys.stderr.flush()

ids = [
'ayrqztr8xkburvvbk3hwj8ybj8dsdnv2', #audris1
'jjd8nkcx3sjr6weurtjqun4hp6b5p7vk', #josh
'2umhecdk2r3hxzvwuy2rx5x4rjeb427x', #camlle
'4frhp5dwf7jnze6dhxdj39ujhdbkygft', #eric
'3n3hce6yq6kz2r2h9mgbqc85rwy5r8qp', #chris
'cx64t5vm27e2pzgwqaqvs2fsxhsrhd73', #John
'cv8rzqn82xq9uub7ybta4y69jxfyfmjb', #david
'ceddqsjxbbjmrvzzuha3eatmewtyfu4e', #fdac3
'4s53en4vju5pn7bde32bkp9f84pu2euf', #bryan
'scfmbawtvvcgny7rnnvnvzuwy84p9p2z', #fdac0
'vcgmh4xc7xnp7ddmr39mz8e8qcw9athf', #fdac00
'5qpn46js8z762ftj9crnrqrqbxn8kgtf', #fdac01
'brb2n4nc42zwmgxxcpgwvbhsjygcqz8f' #collect0
]

id = {
'ayrqztr8xkburvvbk3hwj8ybj8dsdnv2': '9euf9EHR4VsTU4z3PkhvZkpztMFZVB6YBGUPscRR7rR', #audris1
'jjd8nkcx3sjr6weurtjqun4hp6b5p7vk': 'NNHSen7PqBXvyFneKvq4DvDetng6dU8kKZe8pYbx8E9', #josh
'2umhecdk2r3hxzvwuy2rx5x4rjeb427x': 'fDsRmHDRmuAYUmqCHzRu4pqTrfNSDUfzk3BEK8c9cph', #camlle
'4frhp5dwf7jnze6dhxdj39ujhdbkygft': 'DCceK33p3pc5YhpgYTBxGqFaax6ENHufsb4pKPMksj7', #eric
'3n3hce6yq6kz2r2h9mgbqc85rwy5r8qp': '2kkHbMQVvsEPXSk98VE3Cyd5cHMEYqzyHq82rutHe9A', #chris
'cx64t5vm27e2pzgwqaqvs2fsxhsrhd73': 'yut7ya9PpYUkeDTtgRcdCH87Ee4eMXGXA5MK32GtWx5', #John
'cv8rzqn82xq9uub7ybta4y69jxfyfmjb': 'WMbJFvksTUMgHFDTaCNtA9CRHmc8P6RhSUvXtF6cfny', #david
'ceddqsjxbbjmrvzzuha3eatmewtyfu4e': 'anTg7weEWNFJgnK2tY8A9pCzuCeAQQYJwnV4bXYW7kh', #fdac3
'4s53en4vju5pn7bde32bkp9f84pu2euf': 'P2tjx4j758n6yBqpNQaTx97HPrAuCE3sUGEW8fAzuhC', #bryan
'scfmbawtvvcgny7rnnvnvzuwy84p9p2z': 'W73jQG92nAcRa96y27UjDr2cRZcWhW2P73UG5cDMGQE', #fdac0
'vcgmh4xc7xnp7ddmr39mz8e8qcw9athf': 'rJWuzQjpCEBGrtYhFJHDFMdXt7MRaMQN7AJ8cUv5bxF', #fdac00
'5qpn46js8z762ftj9crnrqrqbxn8kgtf': 'rJWuzQjpCEBGrtYhFJHDFMdXt7MRaMQN7AJ8cUv5bxF', #fdac01
'brb2n4nc42zwmgxxcpgwvbhsjygcqz8f': 'jXZDAwPKfecrdMbwHAMpF5PMSR5SvGUwFRnHFeMdCtp' #collect0
}

AUDRIS_ID = 'smyfv7ec67q7t6jqcfwhrv299x4g4rtv'
AUDRIS_SECRET = 'YGQEzsq877fhjZEEHR79F87EwjCn4ABncYTdvVfQGU8'

RJ_ID = 'njsuxksdpaxjg9rhs6hxjnjvusda57fp'
RJ_SECRET = 'yNrWJMaHF6pam9wj4TEpJcEuGE6dZ49Q3UujBhfRFD3'


MARK_ID = 'bj7tfj5kprxhbz6tmf2nt54at4ewwart'
MARK_SECRET = 'UWjzTKEbuA5fsMjr3hEbSjrEGFUmHZKMTbAXeDJCyAB'

MOHAMMAD_ID = 'j2dggcjxqtqummxhhjgbh695qqtheh7x'
MOHAMMAD_SECRET = 'KbbwkCBedJgt6FTgSMvc2NKU5KRABchA9gSeBzQ65Qq'

DEBUG_ID = 'bn5tf5r8j7qdrbqjn5tpq9r3wdsvmr74'
DEBUG_SECRET = 'shuWPNWWH3zhpw2k5seE9WJMY7HHa7x3xShYR5nv9Ya'


IDs = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

i = int(sys.argv[1])
key = ids [i]
val = id [key]
print str(i) +';' + key + ';' + val
thread_proc(key, val, i, IDs)

