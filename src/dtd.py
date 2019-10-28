import flask
import time
import datetime
import threading
import json

app = flask.Flask(__name__, static_url_path='', static_folder='static/')

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
    return flask.send_from_directory("./images", url)

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

#TODO input a single url in the form of a string. Output a list of valid urls. The output may or may not include the startign url. The output url list should be generated using the paper thats linked in the assignment document 
def generateURLs(start_url):
    return [start_url]

#TODO input a single url in the form of a string. Utilize Selenium query the webpage. The results of the query are saved as an array that should be added to "generated_urls" dict in the format of generated_urls[url]=output array
# The format of hte output array should be [http response code, the datetime the query occured, a string url of the saved image so that it can be requsted by the website when it needs ot be rendered.]
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
