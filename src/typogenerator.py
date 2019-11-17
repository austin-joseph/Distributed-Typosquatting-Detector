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

#TODO input a single url in the form of a string. Output a list of valid urls. The output may or may not include the starting url. The output url list should be generated using the paper thats linked in the assignment document 
def generateURLs(start_url):
    output = []
    for x in range(50):
        output.append(start_url + str(x))
    return output

def loop():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT original_url FROM submittedUrls WHERE (processing_finish IS NULL OR TIMESTAMPDIFF(DAY, processing_finish, %s) > 1) AND (processing_start IS NULL OR TIMESTAMPDIFF(SECOND, processing_start, %s) > 2) ORDER BY date_added ASC LIMIT 1", (datetime.datetime.utcnow(),datetime.datetime.utcnow()))
    subCursor = cnx.cursor(buffered=True)
    newUrls = {}
    for x in cursor:
        newUrls[x[0]] = []
        subCursor.execute("UPDATE submittedUrls SET processing_start = %s WHERE original_url = %s", (datetime.datetime.utcnow(), x[0]))
        newUrls[x[0]].extend(generateURLs(x[0]))
        subCursor.execute("UPDATE submittedUrls SET processing_finish = %s WHERE original_url = %s", (datetime.datetime.utcnow(), x[0]))
    
    for originalUrl, generatedUrlList in newUrls.items():
        cursor.execute("SELECT generated_url FROM generatedUrls WHERE original_url = %s", (originalUrl,))
        for x in cursor:
            if x[0] in generatedUrlList:
                generatedUrlList.remove(x[0])
                subCursor.execute("UPDATE generatedUrls SET date_generated = %s WHERE generated_url =  %s", (x[0], datetime.datetime.utcnow()))
        for generatedUrl in generatedUrlList:
            cursor.execute("INSERT INTO generatedUrls (generated_url, original_url, date_generated) VALUES(%s, %s, %s)", (generatedUrl, originalUrl, datetime.datetime.utcnow()))
            
    subCursor.close()
    cursor.close()
    cnx.commit()

def start():
    while True:
        loop()
        time.sleep(1)

def log(message):
    if configFile["logging"] == "True":
        print(message)

cnx = mysql.connector.connect(**configFile["database"])
start()
cnx.close()

