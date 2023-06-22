#!/usr/bin/python3
# script that distributes an archive to web servers
from fabric.api import env, put, run
from os.path import exists, isdir
import os.path
import re

# Set the username and host for SSH connection to the server
env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Distributes archive to web servers
    """
    # Check if the archive file exists
    if not exists(archive_path):
        return False

    # Get the filename from the archive path
    filename = os.path.basename(archive_path)

    # Create the path for storing the archive on the server
    remote_path = "/tmp/{}".format(filename)

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, remote_path)

    # Extract the name of the archive without extension
    folder_name = re.search(r'(.+)\.tgz$', filename).group(1)

    # Create the path for the destination folder on the server
    destination_folder = "/data/web_static/releases/{}".format(folder_name)

    # Create the destination folder if it doesn't exist
    run("mkdir -p {}".format(destination_folder))

    # Uncompress the archive to the destination folder
    run("tar -xzf {} -C {}".format(remote_path, destination_folder))

    # Delete the archive file from the server
    run("rm {}".format(remote_path))

    # Move the contents from the uncompressed folder to the destination folder
    run("mv {}/web_static/* {}".format(destination_folder, destination_folder))

    # Remove the empty web_static folder
    run("rm -rf {}/web_static".format(destination_folder))

    # Delete the existing symbolic link
    run("rm -rf /data/web_static/current")

    # Create a new symbolic link
    run("ln -s {} /data/web_static/current".format(destination_folder))

    print("New version deployed!")
    return True


def deploy():
    """
    Create and distribute the archive to web servers
    """
    # Create the archive using do_pack function
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Deploy the archive using do_deploy function
    return do_deploy(archive_path)


# Usage:
# fab -f 2-do_deploy_web_static.py deploy
