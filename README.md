
# Distributed Typosquatting Detector

DTD is web application designed to help users look out for typosquatters(websites with domain names similar to popular websites mean to decieve users). And warn people of what they might look like.

## Technology Stack 
DTD is made of three seperate python applications, a mysql database and a selenium grid whcih chromium nodes avaliable.

#### Global Prerequisites
```
Python Version: 3.7.7-buster
mysql-connector-python 8.0.18

MySQl Community Edition 8.0.18
```
### Web Server 
Presents a webpage to users allowing them to submit new URLs to DTD and to see the results of previously submitted URLs.
Takes in a single argument a json file check out example file for format

#### Prerequisites
```
Flask 1.1.2
waitress 1.4.4
```

### Typo Generator
Generates possible typo URLs from a source URL based on Section 3.1 of [this](https://www.usenix.org/legacy/event/sruti06/tech/full_papers/wang/wang.pdf) paper.

### Url Verifier
Takes the list of generated typo URLs and queries each one to determine if they are a valid website. Saves a screenshot of the returned website to server to users at a later date.
Takes in a single argument a json file check out example file for format

A selenium grid is run as part of this section of the application
#### Prerequisites
```
Requests 2.22.0
Selenium 3.141.0
```

### Selenium Grid
```
selenium/hub:4.0.0-alpha-7-prerelease-20200826
selenium/node-chrome:4.0.0-alpha-7-prerelease-20200826
```

## SETUP
Each segment of the application has a prebuilt docker container. There are scripts avaliable to setup permissions on linux.
```
1. chmod +x fix_permissions.sh
2. /fix_permissions.sh
3. docker network create dtd-network
4. docker-mysql/build.sh
5. docker-mysql/start.sh
6. src/build_all.sh
7. src/start_all.sh
```

Defaults to port 4000
 
## Current Maintainer

* **[Austin Joseph](https://github.com/austin-joseph)**

## Original Authors

* **[Austin Joseph](https://github.com/austin-joseph)**
* **[Gao XiangShuai](https://github.com/GAO23)**
* Timothy Yuen
* **[Yehonathan Litman](https://github.com/yehonathanlitman)**
