import sys, re, pymongo, json, time
import datetime
from requests.auth import HTTPBasicAuth
import requests

token = '14f3b52b858ec10df24ee0e2fb59cc270a1f4c84'

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client ['strava']

baseurl = 'https://www.strava.com/api/v3/athletes'
#do for ... 
collName = 'athletes'
if (len (sys .argv) > 1):
  collName = sys .argv [1]
# Reference a particular collection in the database
coll = db [collName]

def get (url):
  global token, gleft
  array = None
  size = 0
  # sys.stderr.write ("left:"+ str(left)+"s\n")
  try: 
    r = requests .get (url, headers= { 'Authorization': 'access_token '+ token} )
    sleft, lleft = r.headers.get ('X-RateLimit-Usage').split(',')
    sleft1, lleft1 = r.headers.get ('X-RateLimit-Limit').split(',')
    gleft = int (lleft1) - int(lleft)
    sys.stderr.write ("used:"+ sleft + "," + lleft + " " + sleft1 + "," + lleft1 + " " + str(gleft)+"s\n")
    time .sleep (1)
    if (r.ok):
      lll = r.headers.get ('Link')
      links = ['']
      if lll is not None: 
        links = lll.split(',')
      t = r.text
      size += len (t)
      array = json.loads (t)
      print url + ';' + t
    else:
      print url + ';ERROR'
    if (gleft < 100):
      time .sleep (36*24)
  except requests.exceptions.ConnectionError:
    print url + ';ERROR'
  return array, size

def chunks(l, n):
  if n < 1: n = 1
  return [l[i:i + n] for i in range(0, len(l), n)]

coll = db [collName]
for n in xrange(9,900000):
  nn = str (n)
  url = baseurl + '/' + nn
  url1 = url
  v = []
  size = 0
  try: 
    v, size = get (url1)
  except Exception as e:
    sys.stderr.write ("Could not get:" + url1 + "\n")    
    print e
    continue    
  ts = datetime.datetime.utcnow()
  if v is not None:
    # size may be bigger in bson, factor of 2 doesnot always suffice    
    coll.insert ( { 'name': n, 'url': url, 'utc':ts, 'values': v } )


