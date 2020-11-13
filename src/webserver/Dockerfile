FROM node:15.1 as build-client
WORKDIR /usr/src/app
COPY client/package.json client/yarn.lock ./
RUN yarn
COPY client/public/ ./public
COPY client/src/ ./src
RUN yarn build

FROM python:3.7.7-buster
RUN pip3 install flask==1.1.2 && pip3 install mysql-connector-python==8.0.18 && pip3 install waitress==1.4.4
COPY run.sh /usr/bin/dtd/
RUN chmod +x /usr/bin/dtd/run.sh
COPY config.json /usr/bin/dtd/
COPY webserver.py /usr/bin/dtd/
COPY --from=build-client /usr/src/app/build/ /usr/bin/dtd/static

WORKDIR /usr/bin/dtd
ENTRYPOINT ./run.sh