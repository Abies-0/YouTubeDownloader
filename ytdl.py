import os
import re
import time
from pytube import YouTube

class YouTubeDownloader:

    def __init__(self):
        self.urls = self.read_file()

    def read_file(self):
        fn = "url.txt"
        if not os.path.exists(fn):
            return
        with open (fn, "r") as f:
            urls = f.readlines()
            res_urls = []
            for url in urls:
                url = url.strip()
                if url.startswith("http"):
                    res_urls.append(url)
        return res_urls

    def dl_files(self, type, hq=True):
        if not self.urls:
            return
        if type != "audio" and type != "video":
            return
        for url in self.urls:
            yt = YouTube(url)
            dl_file = yt.streams.filter(type=type, mime_type="%s/mp4" % (type))
            target = dl_file.order_by("abr").desc().first() if hq == True else dl_file.order_by("abr").asc().first()
            name = "%s.mp4" % (re.sub(r'[\\/:*?"<>|]', "", yt.title))
            ts = time.perf_counter()
            target.download(filename=name)
            te = time.perf_counter()
            print("file: {}, download time: {} sec.".format(name, te - ts))
            time.sleep(1)