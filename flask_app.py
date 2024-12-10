# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, Response, redirect
import os, subprocess
import requests
import json
#from opencc import OpenCC

from logging.config import dictConfig

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                "datefmt": "%y%m%d,%H:%M:%S"
            }
        },
        "handlers": {
            #"console": {
            #    "class": "logging.StreamHandler",
            #    "stream": "ext://sys.stdout",
            #    "formatter": "default",
            #},
            "time-rotate": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "pflask.log",
                "when": "D",
                "interval": 10,
                "formatter": "default",
            },
            #"file": {
            #    "class": "logging.FileHandler",
            #    "filename": "plask.log",
            #    "formatter": "default",
            #},
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["time-rotate"],
        },

    }
)


from logging.config import dictConfig


app = Flask(__name__)

#@app.route('/epg', methods=['GET'])
#@app.route('/')
@app.get('/epg')

def epg_get():

    epg_name = ''
    epg_date = ''

    if request.args.get("ch"):
        epg_name = request.args.get('ch')
    if request.args.get("date"):
        epg_date = request.args.get('date')

    if epg_name == '':
        return epg_name

    #cc = OpenCC('t2s')
    app.logger.debug("A debug message")

    #return epg_name
    #epg_url = "http://epg.112114.xyz/?ch=" + cc.convert(epg_name) + "&date=" + epg_date
    epg_url = "http://epg.112114.xyz/?ch=" + epg_name + "&date=" + epg_date

    app.logger.info("quiry: %s", epg_url)

    epg_name = "精彩節目"
    epg_data = "{\"date\":\"" + epg_date + "\",\"channel_name\":\"" + epg_name + "\",\"url\":\"epg.112114.xyz\",\"epg_data\":[{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"00:00\",\"end\":\"02:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"02:00\",\"end\":\"04:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"04:00\",\"end\":\"06:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"06:00\",\"end\":\"08:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"08:00\",\"end\":\"10:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"10:00\",\"end\":\"12:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"12:00\",\"end\":\"14:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"14:00\",\"end\":\"16:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"16:00\",\"end\":\"18:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"18:00\",\"end\":\"20:00\"},{\"title\":" + \
    json.dumps (epg_name) + ",\"start\":\"20:00\",\"end\":\"22:00\"},{\"title\":" + \
    json.dumps (epg_name) +  ",\"start\":\"22:00\",\"end\":\"23:59\"}]}"
    #epg_data = "{date:" + epg_date + ",channel_name:" + epg_name + ",url:epg.112114.xyz,epg_data:[{title:" + epg_name + ",start:00:00,end:23:59}]}"
    return epg_data
    #return json.dumps(epg_data)


    return redirect(epg_url)




@app.get('/yt')

def yt_get():

    yurl = ''

    if request.args.get("url"):
        yurl = request.args.get('url')

    app.logger.info(
        "Get | %s", yurl
    )


    res = requests.request(  # ref. https://stackoverflow.com/a/36601467/248616
        method          = request.method,
        #url             = request.url.replace(request.host_url, url),
        url             = yurl,
        headers         = {k:v for k,v in request.headers if k.lower() != 'host'}, # exclude 'host' header
        data            = request.get_data(),
        cookies         = request.cookies,
        #allow_redirects = False,
        allow_redirects = True,
    )

    #region exlcude some keys in :res response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']  #NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1 ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
    headers          = [
        (k,v) for k,v in res.raw.headers.items()
        if k.lower() not in excluded_headers
    ]
    #endregion exlcude some keys in :res response

    try:
        r = Response(res.content, res.status_code, headers)
        #r.raise_for_status()
    #except requests.exceptions.HTTPError as errh:
    except :
        app.logger.info(
           # "ERROR: %s", errh.args[0]
           "ERROR: %s", res.exceptions
        )
        return "HTTP Error"


    app.logger.info(
        "Resp: %s | %s", headers, res.content
    )
    app.logger.debug(r)

    return r

    #resp = request.get(epg_url, stream=True)
    resp = request.get(url)

    if resp.status_code != 200:
        return Response(resp.content, mimetype=resp.headers.get('Content-Type'))  # 将响应内容作为Flask的Response对象返回
    data = (resp.content)

    return data





@app.route('/')



def hello_world():

    #return "hwllo app.name"
    try:
        file = open('Channel3.m3u', mode='r')
    except OSError as error:
        return ("File {:s} failed".format(error.filename))

    # read all lines at once
    all_of_it = file.read()

    # close the file
    file.close()
    return all_of_it


SCRIPTS_ROOT = '/home/rockercheng/mysite'
@app.route('/run/<script_name>')
def run_script(script_name):
    fp = os.path.join(SCRIPTS_ROOT, script_name)
    try:
        output = subprocess.check_output(['python', fp])
    except subprocess.CalledProcessError as call:
        output = call.output # if exit code was non-zero
    return output.encode('utf-8') # or your system encoding

#if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=8000)



if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0")
