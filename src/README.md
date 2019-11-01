
# Distributed Typosquatting Detector

DTD is made up of three parts.

### Web Server 
Presents a webpage to users allowing them to submit new URLs to DTD and to see the results of previously submitted URLs .

### Url Typo Generator
Generates possible typo URLs from a source URL based on Section 3.1 of [this](https://www.usenix.org/legacy/event/sruti06/tech/full_papers/wang/wang.pdf) paper.

### Url Typo Tester
Takes the list of generated typo URLs and queries each one to determine if they are a valid website. Saves a screenshot of the returned website to server to users at a later date.

## Getting Started

### Prerequisites
```
Python Version: 3.7.4-buster (https://www.python.org/downloads/)
Flash (pip install Flask)
```

## Authors

* **[Austin Joseph](https://github.com/austinobejo)**
* **[Gao XiangShuai](https://github.com/GAO23)**
* **[Timothy Yuen](https://github.com/austinobejo)**

