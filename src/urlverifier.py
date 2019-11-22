import time
import datetime
import json
import sys
import mysql.connector

if len(sys.argv) < 2:
    print("Required Args: config.json")
    exit()
with open(sys.argv[1]) as configHandle:
    configFile = json.load(configHandle)
if configFile == None:
    print("Error loading config file aborting")
    exit()

cnx = None

#TODO input a single url in the form of a string. Utilize Selenium query the webpage. The results of the query are saved as an array that should be added to "generated_urls" dict in the format of generated_urls[url]=output array
# The format of hte output array should be [http response code, the binary data of the saved image so that it can saved by the application and served when the user calls for it.]
def checkURL(url):
    return [9999, None]

def loop():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT generated_url FROM generatedUrls WHERE (processing_finish IS NULL OR TIMESTAMPDIFF(DAY, processing_finish, %s) > 1) AND (processing_start IS NULL OR TIMESTAMPDIFF(SECOND, processing_start, %s) > 2) ORDER BY date_generated ASC LIMIT 1", (datetime.datetime.utcnow(),datetime.datetime.utcnow()))
  
    subCursor = cnx.cursor(buffered=True)
    newResults = {}
    for x in cursor:
        newResults[x[0]] = []
        subCursor.execute("UPDATE generatedUrls SET processing_start = %s WHERE generated_url = %s", (datetime.datetime.utcnow(), x[0]))
        newResults[x[0]].extend(checkURL(x[0]))
        subCursor.execute("UPDATE generatedUrls SET processing_finish = %s WHERE generated_url = %s", (datetime.datetime.utcnow(), x[0]))
    subCursor.close()
    for generatedUrl, urlResults in newResults.items():
        cursor.execute("UPDATE generatedUrls SET generated_image = %s, http_response_code = %s WHERE generated_url = %s", (urlResults[1],urlResults[0], generatedUrl))
            
    cursor.close()
    cnx.commit()

def start():
    while True:
        loop()
        time.sleep(.1)

def log(message):
    if configFile["logging"] == "True":
        print(message)

cnx = mysql.connector.connect(**configFile["database"])
start()
cnx.close()
