#!/usr/bin/env bash

# This Bash script sets up web servers for the deployment of web_static.

# Install Nginx if not already installed
if ! dpkg -s nginx &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
fi

# Create folders
mkdir -p /data/web_static/shared
mkdir -p /data/web_static/releases/test

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create a symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_text="location /hbnb_static/ {\n\talias /data/web_static/current/;\n\tautoindex off;\n}"
sed -i "/listen 80 default_server;/a\ \n$config_text" "$config_file"

# Restart Nginx
systemctl restart nginx

# Exit with success code
exit 0
