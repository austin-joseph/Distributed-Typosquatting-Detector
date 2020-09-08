docker run -d -p 4442-4444:4442-4444 --net dtd-network --name selenium-hub selenium/hub:4.0.0-alpha-7-prerelease-20200826

docker run -d --net dtd-network --name selenium-chrome-0 -e SE_EVENT_BUS_HOST=selenium-hub -e SE_EVENT_BUS_PUBLISH_PORT=4442 -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 --shm-size 2g -e START_XVFB=false selenium/node-chrome:4.0.0-alpha-7-prerelease-20200826

docker run -d --net dtd-network --name selenium-chrome-1 -e SE_EVENT_BUS_HOST=selenium-hub -e SE_EVENT_BUS_PUBLISH_PORT=4442 -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 --shm-size 2g -e START_XVFB=false selenium/node-chrome:4.0.0-alpha-7-prerelease-20200826

docker run -d --net dtd-network --name selenium-chrome-2 -e SE_EVENT_BUS_HOST=selenium-hub -e SE_EVENT_BUS_PUBLISH_PORT=4442 -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 --shm-size 2g -e START_XVFB=false selenium/node-chrome:4.0.0-alpha-7-prerelease-20200826

docker run -d --net dtd-network --name selenium-chrome-3 -e SE_EVENT_BUS_HOST=selenium-hub -e SE_EVENT_BUS_PUBLISH_PORT=4442 -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 --shm-size 2g -e START_XVFB=false selenium/node-chrome:4.0.0-alpha-7-prerelease-20200826

docker run -d --net dtd-network --name selenium-chrome-4 -e SE_EVENT_BUS_HOST=selenium-hub -e SE_EVENT_BUS_PUBLISH_PORT=4442 -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 --shm-size 2g -e START_XVFB=false selenium/node-chrome:4.0.0-alpha-7-prerelease-20200826
