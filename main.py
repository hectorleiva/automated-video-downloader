import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "./vendored"))

from youtube_dl import main as youtube_downloader

PLAYLIST_URL = os.getenv('PLAYLIST_URL')
if not PLAYLIST_URL:
    print('Unable to continue, no PLAYLIST_URL environment variable was set')
    sys.exit(1)

DOWNLOAD_DIR = 'download-videos'

youtube_downloader(
    [PLAYLIST_URL
     , '--ignore-errors'
     , '--download-archive'
     , '{}/archive.txt'.format(DOWNLOAD_DIR)
     , '-r'
     , '2M'
     , '-o'
     , '{}/%(title)s-%(id)s.%(ext)s'.format(DOWNLOAD_DIR)]
)
