import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "./vendored"))

from youtube_dl import main as youtube_downloader

PLAYLIST_URL = os.getenv('YOUTUBE_PLAYLIST_URL')
if not PLAYLIST_URL:
    print('Unable to continue, no YOUTUBE_PLAYLIST_URL environment variable was set')
    sys.exit(1)

DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR')
if not DOWNLOAD_DIR:
    print('Unable to continue, no DOWNLOAD_DIR environment variable was set')
    sys.exit(1)

# Currently unable to download more than one video at a time
youtube_downloader(
    [PLAYLIST_URL
     , '--ignore-errors'
     , '--download-archive'
     , '{}/archive.txt'.format(DOWNLOAD_DIR)
     , '-r'
     , '2M'
     , '-o {}/%(title)s-%(id)s.%(ext)s'.format(DOWNLOAD_DIR)]
)
