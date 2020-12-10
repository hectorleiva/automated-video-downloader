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


### Kubernetes Cronjob Spec

Here's my example of my Kubernetes Cronjob YAML file 

```bash
---
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: automated-video-downloader
  labels:
    app: automated-video-downloader-cronjob
spec:
  schedule: "*/30 * * * *"  # every 30 minutes
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      ttlSecondsAfterFinished: 100  # after 100 seconds, this container should be terminated
      template:
        metadata:
          name: automated-video-downloader-app
          labels:
            app: automated-video-downloader-app
        spec:
          containers:
            - name: automated-video-downloader
              image: hectorleiva/automated-video-downloader:edge
              env:
                - name: PLAYLIST_URL
                  value: "https://www.youtube.com/playlist?list=XXXXXXXXXXXXXXXX"

              volumeMounts:
                - name: custom-apps-nfs # This name matches the claimName, but you can call it whatever you want as long as it matches the claimName.
                  mountPath: "/app/downloaded-videos"
                  subPath: "path/where/you/want/the/videos/to/end/up"

          volumes:
            - name: custom-apps-nfs # This is my name for this volume, you can call it whatever you want
              persistentVolumeClaim:
                claimName: "custom-apps-nfs" # This is my claimName for this volume, you can call it whatever you want

          restartPolicy: Never
```

* Cronjob is used since what we want is for the container. The container will run the `youtube-dl` wrapper and pass the `PLAYLIST_URL` and start downloading the videos on the playlist.
* The `volumes` is set-up beforehand, for this to work you'll need your own [volume](https://kubernetes.io/docs/concepts/storage/volumes/) and volumeMounts set-up.
* We never want this container to try and restart to attempt to redownload, it is fine if it fails and the container completes or errors out.

#### Kubernetes Cronjob won't delete your completed containers

This seems to be an ongoing issue where after a container is completed by a Cronjob, Kubernetes does not delete them.

Instead I did the following to side-step this issue:

* Add `spec.jobTemplate.spec.template.metadata.labels.app` to the Container that will be created by the Cronjob, it is called `automated-video-downloader-app`.
* `ssh`-ed into the Master Kubernetes Node (any other worker node should work, but this made sense to me).
* Create a file called `cleanup-pods.sh`, you can call it whatever you want as long as you keep track of the name.
* Add the following into the file:
```bash
#!/bin/bash

# Deletes the pods that are generated from the kubernetes cronjob
kubectl delete pods -l app=automated-video-downloader-app -n custom-apps
```
* Make sure that the script is executable: `chmod +x cleanup-pods.sh`
* Use `crontab -e` and added the following:
```bash
15 * * * * /home/YOUR_USERNAME_HOME/cleanup-pods.sh
```
