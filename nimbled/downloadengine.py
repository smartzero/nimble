#!/usr/bin/python
# -*- encoding: utf-8 -*-
# pylint: disable=invalid-name,missing-docstring,bad-builtin
from random import randrange
import wget
import threading
import requests
import os
import time

def createTmpName():
    prefix = 'nimbletmp-'
    while True:
        name = prefix + str(randrange(10**5))
        if not os.path.exists(name):
            return name

class Download(object):
    # lo=0, hi=None, filename=None, callback=lambda *args: None
    def __init__(self, url, **kwargs):
        self.url = url
        self.ofile = {
            'name': kwargs.get('filename', wget.extractFilename(url) or createTmpName()),
            'open': False,
            'size': 0,
        }
        with open(self.ofile['name'], 'ab') as _:
            pass
        self.ofile['size'] = os.path.getsize(self.ofile['name'])
        self.start = int(kwargs.get('start', 0))
        self.end = int(kwargs.get('end', wget.downloadSize(url)))
        self.stopflag = False
        self.callback = kwargs.get('callback', lambda *args, **kwargs: None)

    def resume(self):
        self.stopflag = False
        resp = requests.get(self.url, stream=True, headers={'Range': 'bytes={}-{}'.format(self.start, self.end)})
        print "resp.status_code =", resp.status_code
        if 200 <= resp.status_code < 300:
            with open(self.ofile['name'], 'ab') as out:
                for chunk in resp.iter_content(1024*4):
                    out.write(chunk)
                    self.ofile['size'] = out.tell()
                    self.callback(self.ofile['size'], self.end - self.start)
                    if self.stopflag:
                        break

    def pause(self):
        self.stopflag = True

    def status(self):
        return {
            'url': self.url,
            'start': self.start,
            'end': self.end,
            'stopflag': self.stopflag,
            'ofile': self.ofile
        }


class DownloadThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.download = Download(*args, **kwargs)
        self.jobid = str(hash((time.time(), self.name)))
        # get the flask logger and log the args and kwargs

    def run(self):
        self.download.resume()

threads = []

def run(app, cmd):
    app.logger.info(cmd)
    threads.append(DownloadThread(
        cmd['url'],
        filename=cmd.get('filename'),
        start=cmd['start'],
        end=cmd['end']))
    threads[-1].start()
    return threads[-1].jobid

def query(cmd):
    return [thread for thread in threads if thread.jobid == cmd['jobid']][0].download.status()
