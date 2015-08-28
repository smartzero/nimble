from flask import Flask, request, Response, send_file
import downloadengine
import json

CLIENT_DESCRIPTION = {
    u"name": u"eve"
}

WELCOME_MESSAGE = {
    u"msg": u"welcome",
    u"description": CLIENT_DESCRIPTION
}

app = Flask(u"eve")

@app.route("/files/<jobid>")
def getFile(jobid):
    return send_file(downloadengine.query({'jobid': jobid})['ofile']['name'])

@app.route("/query", methods=["POST"])
def query_command():
    return Response(
        json.dumps(downloadengine.query(
            json.loads(request.data.decode(u"utf-8"))[u"downloadengine"])),
        mimetype='application/json; charset=utf-8')

@app.route("/run", methods=["POST"])
def run_command():
    app.logger.info(u"request.headers = %s", repr(request.headers))
    jobid = downloadengine.run(app, json.loads(request.data.decode(u"utf-8"))[u"downloadengine"])
    # subprocess.call(json.loads(request.data.decode(u"utf-8"))[u"cmd"], shell=True)
    return Response(json.dumps({"jobid": jobid}), mimetype='application/json; charset=utf-8')

@app.route("/")
def welcome():
    return json.dumps(WELCOME_MESSAGE)

app.run(debug=True)
