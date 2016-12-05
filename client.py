#!/usr/bin/env python

from urlparse import urljoin
from datetime import datetime
import logging
import platform
import urllib
import sys
import os
import os.path
import shutil

import pytz
import patoolib

# ______________ Helpers _____________

def save_to_movit(url=None, dir_name=None, dl_date=None, path=None,
                    processed=None, **kwargs):
    """Save an Episode to your movit server
    Mandatory:
    :param url:
        Movit server endpoint
        (e.g. `http://movit.example.org/episode/add/`)
    :param dir_name:
        Name of the directory that contains episode
    :param dl_date:
        Date of the download
    :param path:
        Path in which the directory resides
    :param processed:
        Mark the episode as correctly processed
    """

    data = {
        "dir_name": dir_name,
        "dl_date": datetime.now(pytz.utc),
        "path": path,
        "processed": processed,
    }

    data.update(kwargs)

    f = urllib.urlopen(url, urllib.urlencode(data))

    response = f.read()
    status = f.getcode()

    f.close()

    if status == 202:
        logging.debug("Server %s: HTTP %s: %s", url, status, response)
    else:
        raise IOError("Server %s returned HTTP %s" % (url, status))

def process_file(path, filename, dest):
    print "Processing File"
    try:
        shutil.copy2(os.path.join(path, filename), os.path.join(dest, filename))
        return True
    except IOError, e:
        logging.error("Unable to copy file. %s" % e)
        return False

def process_rar(path, filename, dest):
    print "Processing RAR"
    try:
        patoolib.extract_archive(os.path.join(path, filename), outdir=dest,
                                    interactive=False)
        return True
    except patoolib.util.PatoolError, e:
        logging.error("Unable to decompress file. %s" % e)
        return False

process = {
    ".mkv": process_file,
    ".mp4": process_file,
    ".rar": process_rar,
}

# ______________ Config _____________

url = "http://127.0.0.1:8000/frontend/episode/add/"
watch_dirs = ["/path/to/dir"]
dest_dir = "/path/to/dest"
extensions = tuple([".mkv", ".mp4", ".rar"])

# ______________ Main _____________

if __name__ == "__main__":

    torrent_id = sys.argv[1]
    torrent_name = sys.argv[2]
    save_path = sys.argv[3]

    print save_path

    full_path = os.path.join(save_path, torrent_name)
    dest = os.path.realpath(dest_dir)

    processed = False

    #TODO Account for torrents that do not have folders and directly have mkvs
    #if not isdir

    # If path is in watched paths
    if os.path.realpath(save_path) in (os.path.realpath(p) for p in watch_dirs):
        # Walk directory
        for dirpath, dirnames, filenames in os.walk(full_path):
            # For desired file extensions process files
            for filename in [f for f in filenames if f.endswith(extensions)]:
                extension = os.path.splitext(filename)[1]

                # Do not process samples
                if not "sample-" in filename:
                    processed = process[extension](dirpath, filename, dest)

                    # If there is an error bail and report error
                    if not processed:
                        try:
                            pass
                            #save_to_movit(url, save_path, None, save_path, processed)
                            sys.exit(0)
                        except StandardError, e:
                            logging.error("Error saving results: %s", e)
                            sys.exit(1)

        # If everything was processed correctly report result
        try:
            pass
            #save_to_movit(url, save_path, None, save_path, processed)
            sys.exit(0)
        except StandardError, e:
            logging.error("Error saving results: %s", e)
            sys.exit(1)

    else:
        pass
