# automated-video-downloader
A simple program that leverages the youtube-dl program to automate downloading of specific video content to another location

Despite the name of the library used, [youtube-dl](https://youtube-dl.org/) is capable of downloading from [many different video streams](https://ytdl-org.github.io/youtube-dl/supportedsites.html).

## .env
For example
```bash
PLAYLIST_URL=https://www.youtube.com/playlist?list=xxxxxxxxxxxx
```

The `PLAYLIST_URL` must be accessible without authorization for this to work.
