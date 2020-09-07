# automated-video-downloader
A simple program that leverages the youtube-dl program to automate downloading of specific video content to another location

Despite the name of the library used, [youtube-dl](https://youtube-dl.org/) is capable of downloading from [many different video streams](https://ytdl-org.github.io/youtube-dl/supportedsites.html).

## .env
For example
```bash
PLAYLIST_URL=https://www.youtube.com/playlist?list=xxxxxxxxxxxx
```

The `PLAYLIST_URL` must be accessible without authorization for this to work.


## Starting the App

Create the image:
```bash
docker build . -t automated-video-downloader
```

Create the container:
```bash
docker run -dt \
--env-file=.env \
-v automated-videos-downloader-volume:/app/downloaded-videos \
--name automated-video-downloader-app \
automated-video-downloader
```

A cronjob, for example, should then be able to execute this container at will.
```bash
docker start automated-video-downloader-app
```

Every time this container is run, it will:
- Check for new videos  against the `archive.txt` file (in this case `automated-videos-downloader-volume`)
- Any new videos that have been added to the playlist will be downloaded
- `archive.txt` will be updated with the new video file names
