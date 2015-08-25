#!/usr/bin/python
# -*- encoding: utf-8 -*-
# pylint: disable=invalid-name,missing-docstring,bad-builtin
import subprocess

# check if the url supports partial download
def checkPartialSupport(url):
    pass

def run(app, cmd):
    app.logger.info(cmd)

    subprocess.call(u"wget -c " + cmd[u"url"], shell=True)


