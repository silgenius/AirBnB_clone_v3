#!/usr/bin/python3

"""
 Fabric script (based on the file 2-do_deploy_web_static.py) that creates
 and distributes an archive to your web servers, using the function deploy
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
    result = local(command, capture=True)

    # Check if the archive was created successfully
    if result.failed:
        return None
    else:
        return archive_name

def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive file name and its base name without extension
        archive_file = os.path.basename(archive_path)
        archive_no_ext = archive_file.split('.')[0]

        # Define target paths
        tmp_path = f'/tmp/{archive_file}'
        release_path = f'/data/web_static/releases/{archive_no_ext}/'

        # Upload the archive to the /tmp/ directory
        sudo(archive_path, tmp_path)

        # Create the release directory
        sudo(f'mkdir -p {release_path}')

        # Uncompress the archive
        sud(f'tar -xzf {tmp_path} -C {release_path}')

        # Move the contents out of the extracted folder
        sudo(f'mv {release_path}web_static/* {release_path}')
        sudo(f'rm -rf {release_path}web_static')

        # Delete the archive from the web server
        sudo(f'rm {tmp_path}')

        # Delete the old symbolic link
        sudo('rm -rf /data/web_static/current')

        # Create a new symbolic link
        sudo(f'ln -s {release_path} /data/web_static/current')

        return True

    except Exception as e:
        return False

def deploy():
    """
    a Fabric script (based on the file 2-do_deploy_web_static.py) that creates
    and distributes an archive to your web servers, using the function deploy
    """
    archive_path = do_pack()
    if archive_path is False:
        return False

    deploy = do_deploy(archive_path)

    return deploy
