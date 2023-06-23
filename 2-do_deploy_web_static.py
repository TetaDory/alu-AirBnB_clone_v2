#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import env, put, run
from os.path import exists

# Set the username and target servers
env.user = "ubuntu"
env.hosts = ['34.224.66.109', '3.95.37.145']
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """Function to distribute an archive to your web servers"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(path_name))
        run('tar -xzf /tmp/{} -C {}/'.format(file_name, path_name))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(path_name, path_name))
        run("rm -rf {}/web_static".format(path_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path_name))

        # Create 'hbnb_static' directory if it doesn't exist
        run("mkdir -p /data/web_static/releases/{}/hbnb_static".format(name))

        # Move files from web_static to hbnb_static
        run("mv {}/web_static/* {}/hbnb_static".format(path_name, path_name))

        # Delete the empty web_static directory
        run("rm -rf {}/web_static".format(path_name))

        return True
    except Exception:
        return False
