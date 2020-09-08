#!/usr/bin/python3

import time
import datetime
import json
import sys
import mysql.connector
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import requests
import base64

config_file = None
logging.basicConfig(filename='urlverififer.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

cnx = None

if len(sys.argv) < 2:
    config_file = "./config.json"
    logger.info("config.json not specififed using default")
else:
    config_file = sys.argv[1]
    logger.info("config.json specififed at " + sys.argv[1])

logger.info("loading config file from " + config_file)
with open(config_file) as configHandle:
    configFile = json.load(configHandle)

if configFile == None:
    logger.warning("Error loading config file aborting")
    exit()

#TODO input a single url in the form of a string. Utilize Selenium query the webpage. The results of the query are saved as an array that should be added to "generated_urls" dict in the format of generated_urls[url]=output array
# The format of hte output array should be [http response code, the binary data of the saved image so that it can saved by the application and served when the user calls for it.]
def checkURL(url):
    url = "http://" + url
    opts = Options()
    opts.add_argument("--headless")
    try:
        driver = webdriver.Remote(command_executor=configFile["selenium"]["hub_address"], desired_capabilities=configFile["selenium"]["desired_capabilities"], options=opts)
    except:
        logger.critical("Unexpected error:" + str(sys.exc_info()[0]))
        return None    
    driver.set_page_load_timeout(5)
    driver.maximize_window()
    try:    
        driver.get(url)
    except TimeoutException:
        img = driver.get_screenshot_as_png()
        logger.info("Page Timed Out")
        # print(base64.encodestring(img))
        return [403, base64.encodestring(img)]
    except WebDriverException:
        img = driver.get_screenshot_as_png()
        logger.info("Page Not Found")
        # print(base64.encodestring(img))
        return [404, base64.encodestring(img)]
   
    img = driver.get_screenshot_as_png()
    driver.close()
    try:
        req = requests.get(url)
        return [req.status_code, base64.encodestring(img)]
    except requests.ConnectionError:
        # print(base64.encodestring(img))
        return [503, base64.encodestring(img)] #503 = service unavailable

def loop():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT generated_url,processing_start FROM generatedUrls WHERE (processing_finish IS NULL OR TIMESTAMPDIFF(DAY, processing_finish, %s) > 1) AND (processing_start IS NULL OR TIMESTAMPDIFF(SECOND, processing_start, %s) > 2) ORDER BY date_generated ASC LIMIT %s", (datetime.datetime.utcnow(),datetime.datetime.utcnow(), configFile["max_allowed_tasks_per_update"]))
    subCursor = cnx.cursor(buffered=True)
    newResults = {}
    for x in cursor:
        newResults[x[0]] = []
        subCursor.execute("UPDATE generatedUrls SET processing_start = %s WHERE generated_url = %s", (datetime.datetime.utcnow(), x[0]))
        logger.info("Checking: "+ x[0])
        checkUrlResults = checkURL(x[0])
        if checkUrlResults != None:
            newResults[x[0]].extend(checkUrlResults)
            subCursor.execute("UPDATE generatedUrls SET processing_finish = %s WHERE generated_url = %s", (datetime.datetime.utcnow(), x[0]))
            logger.info("Response Code: "+ str(checkUrlResults[0]))
        else:
            subCursor.execute("UPDATE generatedUrls SET processing_start = %s WHERE generated_url = %s", (x[1], x[0]))
            logger.warning("Urlverifier had an error communicating with selenium.")

    subCursor.close()
    for generatedUrl, urlResults in newResults.items():
        length = len(urlResults)
        if length == 0:
            continue
        length = len(urlResults[1])
        if length > configFile["max_image_size"]:
            cursor.execute("UPDATE generatedUrls SET http_response_code = %s WHERE generated_url = %s", (urlResults[0], generatedUrl))
        else:
            #print(urlResults[1])
            cursor.execute("UPDATE generatedUrls SET generated_image = %s, http_response_code = %s WHERE generated_url = %s", (urlResults[1].decode("utf-8"),urlResults[0], generatedUrl))
        
        cursor.execute("UPDATE generatedUrls SET processing_finish = %s WHERE generated_url = %s", (datetime.datetime.utcnow(), generatedUrl))
            
    cursor.close()
    cnx.commit()

def start():
    logger.info("Starting urlverifier")
    while True:
        loop()

cnx = mysql.connector.connect(**configFile["database"])
start()
cnx.close()
