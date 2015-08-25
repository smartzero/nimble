import urlparse
import urllib
import requests
import cgi
import posixpath
from sys import stdout

def urlretrieve(url, lo, hi, filename, progressbar):
    resp = requests.head(url)
    size = int(resp.headers.get('content-length', '0'))
    urlopener = urllib.FancyURLopener()
    urlopener.addheader('Range', 'bytes={0}-{1}'.format(lo, hi))
    urlopener.urlretrieve(url, filename, progressbar)

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


def download(url, filename=None):
    filename = filename or extractFilename(url)
    # create new file if the filename already exists
    # --
    # # # # # # # # # # # # # # # # # # # # # # # # #
    tmpname = 'tmp01230123.tmp'
    _, result = urlretrieve(url, filename or tmpname, progressbar)
    print

if __name__ == '__main__':
    import sys
    download(sys.argv[1])
