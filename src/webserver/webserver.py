#!/usr/bin/python3
# -*- coding: utf-8 -*-
import flask
import datetime
import json
import sys
import mysql.connector
from flask import Response
import base64
from waitress import serve
import logging
from pythonjsonlogger import jsonlogger
import os
import time

config_file = "config.json"
# loggingDefaults = {
#     "output_file": "./log/full.log",
#     "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# }

if len(sys.argv) < 2:
    config_file = "config.json"
    print("defaulting to " + os.path.abspath(config_file))
else:
    config_file = sys.argv[1]
    print("Loading config at " + os.path.abspath(config_file))

with open(config_file) as configHandle:
    configFile = json.load(configHandle)

if configFile == None:
    print("Error loading config file aborting")
    exit()

# waitresslogger = logging.getLogger('waitress')
# waitresslogger.setLevel(logging.NOTSET)
# waitressHandler = logging.FileHandler(configFile["logging"]["waitress_log"])
# waitressHandler.setLevel(logging.NOTSET)
# waitressHandler.setFormatter(configFile["logging"]["format"])
# waitresslogger.addHandler(waitressHandler)

# rootLogger = logging.getLogger()
# fileHandler = logging.FileHandler(configFile["logging"]["root_log"], mode='a+')
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)

consoleLogFormatter = logging.Formatter(configFile["logging"]["format"])


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        log_record["timestamp"] = datetime.datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        # print("print")
        # print(record.__dict__)
        # print(log_record)


jsonFormatter = CustomJsonFormatter()

mainLogger = logging.getLogger(configFile["logging"]["base_name"]+".core")
mainLogger.setLevel(logging.DEBUG)

mainFileHandler = logging.FileHandler(configFile["logging"]["all_log"])
mainFileHandler.setFormatter(jsonFormatter)
mainFileHandler.setLevel(logging.DEBUG)
mainLogger.addHandler(mainFileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(consoleLogFormatter)
mainLogger.addHandler(consoleHandler)


trafficLogger = logging.getLogger(
    configFile["logging"]["base_name"] + ".traffic")
trafficLogger.setLevel(logging.DEBUG)

trafficFileHandler = logging.FileHandler(configFile["logging"]["traffic_log"])
trafficFileHandler.setFormatter(jsonFormatter)
trafficFileHandler.setLevel(logging.DEBUG)
trafficLogger.addHandler(trafficFileHandler)


mainLogger.info(
    "Creating Flask instance with values {}".format(configFile["flask"]))

app = flask.Flask(__name__, static_url_path=configFile["flask"]["static_url_path"],
                  static_folder=configFile["flask"]["static_folder"])

mainLogger.info({"message": "Attempting to connect",
                 "database": configFile["database"]["host"] + ":" + configFile["database"]["port"]})
cnx = None
for i in range(5):
    try:
        cnx = mysql.connector.connect(**configFile["database"])
    except mysql.connector.Error as err:

        mainLogger.critical("Connection to database: {} failed, attempting to reconnect".format(
            configFile["database"]["host"] + ":" + configFile["database"]["port"]))
        time.sleep(5)
if cnx == None:
    mainLogger.critical("Connection to database: {} failed. Stopping".format(
        configFile["database"]["host"] + ":" + configFile["database"]["port"]))
    exit()


# def logTrafficToBoth(level, message)

@app.route("/", methods=["GET"])
def index():
    message = {"method": "GET", "endpoint": "/",
               "headers": flask.request.headers}
    trafficLogger.info(message)
    mainLogger.info(message)
    return app.send_static_file("index.html")


@app.route("/image/<string:url>", methods=["GET"])
def image(url):
    message = {"type": "request", "method": "GET",
               "endpoint": "/image/<string:url>", "image": url, "headers": flask.request.headers}
    trafficLogger.info(message)
    mainLogger.info(message)
    startTime = time.time()
    cursor = cnx.cursor(buffered=True)
    cursor.execute(
        "SELECT generated_image FROM generatedUrls WHERE generated_url=%s LIMIT 1", (url,))
    image = None
    for x in cursor:
        if x[0] != None:
            image = x[0]
    cursor.close()
    endTime = time.time()
    if image != None:
        message = {"type": "response", "endpoint": "/image/<string:url>",
                   "image": url, "time_elapsed": endTime-startTime, "status": 200}
        trafficLogger.info(message)
        mainLogger.info(message)
        return app.response_class(base64.decodestring(str.encode(image)), mimetype="image/png")
    else:
        message = {"type": "response", "endpoint": "/image/<string:url>", "image": url,
                   "time_elapsed": endTime-startTime, "status": 404, "error": "image not found"}
        trafficLogger.error(message)
        mainLogger.error(message)
        return Response("{'error':'image not found'}", status=404, mimetype='application/json')


@app.route("/view", methods=["POST"])
def viewResults():
    message = {"type": "request", "method": "POST",
               "endpoint": "/view", "submitted_url": flask.request.form["url"], "headers": flask.request.headers}
    trafficLogger.info(message)
    mainLogger.info(message)
    startTime = time.time()
    mainLogger.info("Request on /view")
    givenUrl = flask.request.form["url"]
    responseJson = {}
    responseJson["error"] = 0
    responseJson["inputUrl"] = givenUrl

    query = ("SELECT COUNT(*) FROM submittedUrls WHERE original_url=%s")
    queryData = (givenUrl,)
    cursor = cnx.cursor()
    cursor.execute(query, queryData)

    urlInDatabase = True
    for x in cursor:
        if x[0] <= 0:
            urlInDatabase = False
            break

    if not urlInDatabase:
        responseJson["error"] = 1
        query = (
            "INSERT INTO submittedUrls (original_url, date_added)  VALUES(%s, %s)")
        queryData = (givenUrl, datetime.datetime.utcnow())
        cursor.execute(query, queryData)
        endTime = time.time()
        message = {"type": "response", "endpoint": "/view", "submitted_url": givenUrl,
                   "time_elapsed": endTime-startTime, "error_type": 1, "message": "Url not in database. Adding to submittedUrls"}
        trafficLogger.info(message)
        mainLogger.info(message)
    else:
        query = ("SELECT generated_url, http_response_code, processing_finish, if(generated_image is not null, true, false)image_null FROM generatedUrls WHERE original_url = %s")
        queryData = (givenUrl,)
        cursor.execute(query, queryData)
        responseJson["generatedUrls"] = []
        responseJson["urlQueryResults"] = []
        for x in cursor:
            if x[2] == None:
                responseJson["error"] = 2
                endTime = time.time()
                message = {"type": "response", "endpoint": "/view", "submitted_url": givenUrl, "current_url": x[0],
                           "time_elapsed": endTime-startTime, "error_type": 2, "message": "No response code for generated_url"}
                trafficLogger.info(message)
                mainLogger.info(message)
            if x[1] != None and int(x[1]) >= 200 and int(x[1]) < 300:
                responseJson["generatedUrls"].append(x[0])
                responseJson["urlQueryResults"].append(
                    {
                        "generated_url": x[0],
                        "http_response_code": x[1],
                        "generated_image": "/image/" + str(x[0]) if x[3] == 1 else "#"
                    }
                )
                endTime = time.time()
                message = {"type": "response", "endpoint": "/view", "url": givenUrl, "current_url": x[0],
                           "time_elapsed": endTime-startTime, "error_type": 0, "message": "Response code {} for current url".format(x[1])}
                trafficLogger.info(message)
                mainLogger.info(message)
    cursor.close()
    cnx.commit()
    return json.dumps(responseJson, sort_keys=True, default=str)

if __name__ == "__main__":
    mainLogger.info("Waitress started on port {}".format(
        configFile["flask"]["port"]))
    serve(app, listen='*:'+configFile["flask"]["port"])
