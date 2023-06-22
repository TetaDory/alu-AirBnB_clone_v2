#!/usr/bin/python3
 """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: The path of the generated archive if successful, None otherwise.
"""

from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Define do_pack and
    Returns:
        str: The path of the generated archive if successful, None otherwise.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(now)
 
    local("mkdir -p versions")
 
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.failed:
        return None

    return archive_path
