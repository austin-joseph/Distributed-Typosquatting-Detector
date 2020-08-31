FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3.7 && apt-get install -y python3-pip

RUN pip3 install mysql-connector-python==8.0.18 && pip3 install requests==2.22.0 && pip3 install selenium==3.141.0

COPY chromium-browser/chromium-browser.deb /usr/bin/dtd/cchromium-browser/chromium-browser.deb
RUN apt-get install -y /usr/bin/dtd/cchromium-browser/chromium-browser.deb

COPY urlverifier.py /usr/bin/dtd/
COPY chromedriver /usr/bin/dtd/chromedriver/

COPY run.sh /usr/bin/dtd/
RUN chmod +x /usr/bin/dtd/run.sh

COPY config.json /usr/bin/dtd/

WORKDIR /usr/bin/dtd
ENTRYPOINT ./run.sh