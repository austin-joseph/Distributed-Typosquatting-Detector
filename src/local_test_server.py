import flask
import time
import datetime
import threading
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

if len(sys.argv) < 2:
    print("Required Args: config.json")
    exit()
with open(sys.argv[1]) as configHandle:
    configFile = json.load(configHandle)
if configFile == None:
    print("Error loading config file aborting")
    exit()

app = flask.Flask(__name__, static_url_path='',
                  static_folder=configFile["flask"]["static_folder"])

new_urls_lock = threading.Lock()
new_urls = []
submitted_urls_lock = threading.Lock()
submitted_urls = {}
generated_urls_lock = threading.Lock()
generated_urls = {}

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/image/<string:url>")
def image(url):
    try:
        print(configFile["flask"]["image_folder"]+"/"+url+".image")
        with open(configFile["flask"]["image_folder"]+"/"+url+".image", 'rb') as file:
            fileBytes = file.read()
            return app.response_class(fileBytes, mimetype="image/png")
    except IOError: 
        return None

@app.route("/view", methods=["POST"])

def viewResults():
    # if the url exists in our existing data send back that data. IF it doesnt exist find it.
    givenUrl = flask.request.form["url"]
    responseJson = {}
    responseJson["error"] = 0
    responseJson["inputUrl"] = givenUrl

    submitted_urls_lock.acquire()
    generated_urls_lock.acquire()
    if givenUrl in submitted_urls:
        searchList = submitted_urls[givenUrl][0]
        urlQueryResults = []
        for x in searchList:
            try:
                urlQueryResults.append(
                     {
                        "generated_url" : x,
                        "http_response_code":generated_urls[x][0],
			    		"generated_image" : "/image/" + x
                    }
                )
            except KeyError:
                continue
        responseJson["generatedUrls"]=searchList
        responseJson["urlQueryResults"]=urlQueryResults
    else:
        new_urls_lock.acquire()
        if  givenUrl not in new_urls:
            new_urls.append(givenUrl)
        new_urls_lock.release()        
        responseJson["error"] = 1

    submitted_urls_lock.release()
    generated_urls_lock.release()
    return json.dumps(responseJson, sort_keys=True, default=str)

#TODO input a single url in the form of a string. Output a list of valid urls. The output may or may not include the startign url. The output url list should be generated using the paper thats linked in the assignment document 
def generateURLs(start_url):
    output = []
    for x in range(8):
        output.append(start_url + str(x))
    return output

#TODO input a single url in the form of a string. Utilize Selenium query the webpage. The results of the query are saved as an array that should be added to "generated_urls" dict in the format of generated_urls[url]=output array
# The format of hte output array should be [http response code, the binary data of the saved image so that it can saved by the application and served when the user calls for it.]
def checkURL(url, opts):
    #When you query a website youre supposed to get a screen shot of the webpage and add them to the output array as a list of bytes. Given that this method doesnt actually query anything it gets the byte list from test.png in the images dir. When you actually implement this method dont actually reador write anything to/from file thats already handled.
    url = "http://www." + url
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=opts)
    driver.get(url)
    img = driver.get_screenshot_as_png()
    driver.close()
    try:
        req = requests.get(url)
        return [req.status_code, img]
    except requests.ConnectionError:
        return [503, img] #503 = service unavailable

def checkURLWrapper(url, opts):
    results = checkURL(url, opts)    
    generated_urls_lock.acquire()    
    generated_urls[url] = results
    generated_urls_lock.release()

    if results[1] != None:
        with open(configFile["flask"]["image_folder"]+"/"+url+".png", 'wb') as file:
            file.write(results[1])
        

def scheduler():
    shutdown = False
    currentDateTime = datetime.datetime.utcnow()
    while(True):
        time.sleep(1)
        new_urls_lock.acquire()
        if len(new_urls) <= 0:            
            new_urls_lock.release()
            continue
        listCopy = new_urls.copy()
        new_urls.clear()
        new_urls_lock.release()

        for url in listCopy:        
            generatedUrls = None
            submitted_urls_lock.acquire()
            if url in submitted_urls:            
                #compare current date to the last time we checked. If more than a day has passed redo the sub url generation
                if currentDateTime - submitted_urls[url][1] > datetime.timedelta(days=1):
                    generatedUrls = generateURLs(url)
                    submitted_urls[url][0] = generatedUrls
                    submitted_urls[url][1] = datetime.datetime.utcnow()
            else:            
                generatedUrls = generateURLs(url)
                submitted_urls[url] = [generatedUrls, datetime.datetime.utcnow()]
            submitted_urls_lock.release()

            if generatedUrls != None and len(generatedUrls) > 0:
                opts = Options()
                opts.add_argument("--headless")
                for x in generatedUrls:
                    newThread = threading.Thread(target=checkURLWrapper, args=(x, opts, ), name="Checking: " + x)
                    newThread.start()

try:
    t = threading.Thread(target=scheduler, name="Scheduler")
    t.start()
except:
    print("Error: unable to start thread")

if __name__ == "__main__":
    app.run(port="5000", threaded=True)
