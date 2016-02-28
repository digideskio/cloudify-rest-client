import os
import tarfile
from os.path import expanduser


def tar_blueprint(blueprint_path, tempdir):
    blueprint_path = expanduser(blueprint_path)
    blueprint_name = os.path.basename(os.path.splitext(blueprint_path)[0])
    blueprint_directory = os.path.dirname(blueprint_path)
    if not blueprint_directory:
        # blueprint path only contains a file name from the local directory
        blueprint_directory = os.getcwd()
    tar_path = '{0}/{1}.tar.gz'.format(tempdir, blueprint_name)
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(blueprint_directory,
                arcname=os.path.basename(blueprint_directory))
    return tar_path
