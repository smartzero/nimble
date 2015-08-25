from flask import Flask, request
import downloadengine
import subprocess
import json
CLIENT_DESCRIPTION = {
    u"name": u"eve"
}
WELCOME_MESSAGE = {
    u"msg": u"welcome",
    u"description": CLIENT_DESCRIPTION
}

app = Flask(u"eve")

@app.route("/run", methods=["POST"])
def run_command():
    app.logger.info(u"request.headers = %s", repr(request.headers))
    downloadengine.run(app, json.loads(request.data.decode(u"utf-8"))[u"downloadengine"])
    # subprocess.call(json.loads(request.data.decode(u"utf-8"))[u"cmd"], shell=True)
    return u"successful"

@app.route("/")
def welcome():
    return json.dumps(WELCOME_MESSAGE)

app.run(debug=True)
