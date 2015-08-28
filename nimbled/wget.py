import urlparse
import urllib
import requests
import cgi
import posixpath
from sys import stdout


def urlretrieve(url, lo, hi, filename, callback):
    urlopener = urllib.FancyURLopener()
    urlopener.addheader('Range', 'bytes={0}-{1}'.format(lo, hi))
    return urlopener.retrieve(url, filename, callback)

def downloadSize(url):
    return int(requests.head(url).headers.get('Content-Length', '0'))

def extractFilename(url):
    # extracts filename of url either from headers or from url string
    resp = requests.head(url)
    _, params = cgi.parse_header(resp.headers.get('Content-Disposition', ''))
    return params.get('filename') or posixpath.basename(urlparse.urlsplit(url).path)

def progressbar(blocks, blocksize, totalsize):
    currentsize = min(blocks*blocksize, totalsize)
    completed = currentsize*100 // totalsize
    # print (
    #     '', completed, 100 - completed,
    #     blocks*blocksize, totalsize, completed)
    stdout.write(
        '\r[{0:=<{1}}{0:-<{2}}] {3:>10} / {4:<10} | {5}%'.format(
            '', completed, 100 - completed,
            currentsize, totalsize, completed))
    stdout.flush()

class NonResumableDownload(Exception):
    def __init__(self, *args):
        self.args = args
        super(NonResumableDownload, self).__init__(*args)
    def __repr__(self):
        return repr(self.args)
    def __str__(self):
        return str(self.args)

def checkResumeSupport(url):
    resp = requests.head(url)
    if resp.headers.get(u'Accept-Ranges') == None:
        raise NonResumableDownload(url, resp.headers)

def download(url, filename=None, lo='0', hi=''):
    checkResumeSupport(url)
    filename = filename or extractFilename(url)
    # create new file if the filename already exists
    # --
    # # # # # # # # # # # # # # # # # # # # # # # # #
    tmpname = 'tmp01230123.tmp'
    _, result = urlretrieve(url, lo, hi, filename or tmpname, progressbar)
    print result

if __name__ == '__main__':
    import sys
    download(sys.argv[1])
