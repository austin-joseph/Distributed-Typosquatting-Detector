import flask
import time
import datetime
import threading
import json

app = flask.Flask(__name__, static_url_path='', static_folder='static/')

new_urls_lock = threading.Lock()
new_urls = []
#map of url to a list of the sub urls that exist
submitted_urls_lock = threading.Lock()
submitted_urls = {}
#map of each sub url to related data
generated_urls_lock = threading.Lock()
generated_urls = {}

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/image/<string:url>")
def image(url):
    return flask.send_from_directory("images", url)

@app.route("/view", methods=["POST"])

def viewResults():
    # if the url exists in our existing data send back that data. IF it doesnt exist find it.
    output = {}
    givenUrl = flask.request.form["url"]

    submitted_urls_lock.acquire()
    generated_urls_lock.acquire()
    if givenUrl in submitted_urls:
        searchList = submitted_urls[givenUrl][0]
        tempDict = {}
        for x in searchList:
            tempDict[x]=(generated_urls[x])
        output["urls"]=searchList
        output["data"]=tempDict
        output["done"] = True
    else:
        new_urls_lock.acquire()
        if  givenUrl not in new_urls:
            new_urls.append(givenUrl)
        new_urls_lock.release()
        output["done"] = False

    submitted_urls_lock.release()
    generated_urls_lock.release()
    return json.dumps(output, sort_keys=True, default=str)

def generateURLs(start_url):
    return [start_url]

def checkURL(url):
    generated_urls_lock.acquire()    
    generated_urls[url] = [200, datetime.datetime.utcnow(), "The Image Doesnt Exist"]
    generated_urls_lock.release()

def scheduler():
    shutdown = False
    currentDateTime = datetime.datetime.utcnow()
    while(True):
        time.sleep(1)
        new_urls_lock.acquire()
        if len(new_urls) <= 0:            
            new_urls_lock.release()
            continue
        url = new_urls.pop(0)
        new_urls_lock.release()

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
            for x in generatedUrls:
                newThread = threading.Thread(target=checkURL, args=(x,), name="Checking: " + x)
                newThread.start()

try:
    t = threading.Thread(target=scheduler, name="Scheduler")
    t.start()
except:
    print("Error: unable to start thread")

if __name__ == "__main__":
    app.run(port="5000", threaded=True)
