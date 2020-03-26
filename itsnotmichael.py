import urllib.request
import json 
import time


# It's Not Michael

debug = True

URL = "http://marquee.itsmichael.info/"

MARQUEE_LENGTH_PIXELS = 32
PIXEL_RATE_PER_SECOND = 10 
LETTER_SIZE_PIXELS = 10
LINE_LENGTH_CHARS = 32
alllines = []

def build_message(msg):
    return { "message" : msg }

# read file into string
with open('data.txt', 'r') as file:
    data = file.read().replace('\'','')

datalines = data.split('\n')

# split string into lines 
for dataline in datalines:

    # look for max whitespace position under LINE_LENGTH, otherwise just add the line fragment
    while len(dataline) > LINE_LENGTH_CHARS:
        
        wsPos = dataline[0:LINE_LENGTH_CHARS].rfind(' ')
    
        line = dataline[0:wsPos]    
        #print(line)
        dataline = dataline.replace(line,'')
        
        #lines = [dataline[i:i+wsPos] for i in range(0, len(dataline), LINE_LENGTH)]
        alllines.append(line)
        
    alllines.append(dataline)

if (debug is True):
    print(alllines)

for line in alllines:
    req = urllib.request.Request(URL)
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    jsondata = json.dumps(build_message(line))
    print(jsondata)
    jsondataasbytes = jsondata.encode('utf-8')     
 
    req.add_header('Content-Length', len(jsondataasbytes))	
    
    # send request
    if (debug is False):
        response = urllib.request.urlopen(req, jsondataasbytes)
        print(response)
    
    # calculate how long the request will scroll: chars per second + buffer
    sleepAmount = round((LETTER_SIZE_PIXELS * len(line) + MARQUEE_LENGTH_PIXELS) / PIXEL_RATE_PER_SECOND)
    
    
    if (debug is False):
        time.sleep(sleepAmount)
    else: 
        print("The app will sleep for {} seconds".format(sleepAmount))
        time.sleep(1)