#!/usr/bin/python3
# script that distributes an archive to web servers
from fabric.api import env, put, run
import os


env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<your-username>'
env.key_filename = '<path-to-ssh-key>'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.

    Args:
        archive_path (str): The path of the archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on web servers
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/
        filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/" + filename.split('.')[0]
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))
        run("rm /tmp/{}".format(filename))

        # Move contents of extracted folder to its parent directory
        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True
    except:
        return False
