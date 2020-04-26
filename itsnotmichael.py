import urllib.request
import json 
import time
import random

# It's Not Michael

debug = False

URL = "http://marquee.itsmichael.info/"

MARQUEE_LENGTH_PIXELS = 32
PIXEL_RATE_PER_SECOND = 10 
LETTER_SIZE_PIXELS = 10
LINE_LENGTH_CHARS = 32

all_lines = []
default_colour = "00ff00"

# omg canadians and their "colour" parameter
def build_message(msg, colour):
    return { "colour" : colour, "message" : msg }
    
def random_hex():
    num = random.randint(0,256)
    hexNum = hex(num)
    return str(hexNum).replace('0x','').rjust(2,'0')

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
        all_lines.append(line)
        
    all_lines.append(dataline)

all_lines.append("*****")

if (debug is True):
    print(all_lines)

for line in all_lines:
    # Generate random color
    newcolor = random_hex() + random_hex() + random_hex()
    #print(newcolor)
    
    # Build header and body
    jsondata = json.dumps(build_message(line, newcolor))
    jsondataasbytes = jsondata.encode('utf-8')      
    req = urllib.request.Request(URL)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))	
    
    # Display request
    print(jsondata)
    
    # Send request
    if (debug is False):
        print("Sending line...")
        response = urllib.request.urlopen(req, jsondataasbytes)
        print(response.getcode())
    
    # Calculate how long the request will scroll: chars per second + buffer
    sleepAmount = round((LETTER_SIZE_PIXELS * len(line) + MARQUEE_LENGTH_PIXELS) / PIXEL_RATE_PER_SECOND)
        
    if (debug is False):
        print("Sleeping for {} seconds...".format(sleepAmount))
        time.sleep(sleepAmount)
    else: 
        time.sleep(1)
        