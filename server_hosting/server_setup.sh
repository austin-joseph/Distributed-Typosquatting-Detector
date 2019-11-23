#!/bin/bash

# this is for configuring server hosting on Ubuntu 18.04 servers
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

apt update;
apt dist-upgrade -y;
apt install nodejs -y;
apt install mongodb -y;
apt install apache2 -y;
apt install mysql-server;
systemctl enable mongodb; # just in case if mysql is too much a pain
systemctl start mongodb;
systemctl disable apache2;
systemctl start apache2;
ufw allow 'Apache';
cp ./apache_reverse_proxy.conf /etc/apache2/sites-available/;
a2enmod proxy;
a2enmod proxy_http;
a2enmod proxy_ajp;
a2enmod rewrite;
a2enmod deflate;
a2enmod headers;
a2enmod proxy_balancer;
a2enmod proxy_connect;
a2enmod proxy_html;
a2ensite apache_reverse_proxy.conf;
a2dissite 000-default.conf;
systemctl restart apache2;