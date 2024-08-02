#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static folder of AirBnB Clone repo, using the function do_pack
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    # Create versions directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"versions/web_static_{timestamp}.tgz"

    command = f'tar -czvf {archive_name} web_static'
    result = local(command, capture=False)

    # Check if the archive was created successfully
    if result.failed:
        return None
    else:
        return archive_name
