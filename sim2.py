#!/usr/bin/python3
#
# Copyright (C) 2021, Transpara LLC. All rights reserved.
#
#  simulate values for a bunch of tags
#
#   February 4, 2022 - Inselbuch
#       from older work
#       writes to tstore using tstore-api
#       backfill code converted to regular loop
#       hardcoded for one-minute values
#       includes hostname to support data from multiple hosts
#       takes promURL from environment variable (or defaults)
#       no error checking on tagfile syntax
#       
#

from datetime import datetime,timedelta
import time
import math
import random
import gc
import os
import sys
import socket
import json
import requests
import traceback

hostname = socket.gethostname()
headers = {'Content-Type': 'application/json'}

points = {}

f = open('tagfile.txt','r')
for line in f:
   ls = line.split(',')
   tagname = ls[0]
   typical = ls[1]
   points[tagname]=typical
f.close()

# use the hostname passed in from the host through an env variable in the run command
host_name = os.getenv('host_name',hostname)

# when running inside a container (on the same network as tstore-api)
promURL = os.getenv('promURL','http://tstore-api:80/api/v1/write')

# promscale does not like certain characters
# and there are others that I don't like
def promName(c):
    x = c.lower()
    x = x.replace(' ','_')
    x = x.replace('.','_')
    x = x.replace('/','_')
    return x

# convert time to promscale expectation
def epochInt(etime):
    return int(etime*1000.0)

def send(labels,samples):
    data = {"labels" : labels, "samples" : samples}
    r=requests.request(method='POST',url=promURL,headers=headers,data=json.dumps(data),verify=False,timeout=10)


# for backfilling

#end_time = datetime.now()
#start_time = end_time - timedelta(days=10)\
#ts = start_time
#while ts < end_time:

# for regular operation
ts = datetime.now()
while True:

   # FOR DAILY VALUES ONLY AT MIDNIGHT
   #x = ts.replace(hour=0,minute=0,second=0,microsecond=0)

   for p in points:
      tagname = p
      typical = float(points[p])
      #v = random.random()*typical
      v = typical * 0.95 + random.random()*typical*0.10

      now = epochInt(datetime.now().timestamp())

      labels = {"__name__": 'carbon','hostname':host_name,'tagname':tagname }
      samples = [[now,v]]
      send(labels,samples)


   # for backfilling
   #   ts = ts + timedelta(minutes=5)
   #time.sleep(0.1)

   # for regular operation (new value twice a day)
   time.sleep(43200)

