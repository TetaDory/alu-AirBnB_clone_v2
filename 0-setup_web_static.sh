#!/usr/bin/env bash
# This Bash script sets up web servers for the deployment of web_static.

if ! dpkg -s nginx &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
fi

mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

rm -rf /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

chown -R ubuntu:ubuntu /data/

sudo sed -i '44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

systemctl restart nginx
exit 0
