from flask import Flask, request, jsonify
import json
import requests
import logging
import os

logger = logging.getLogger("Max's MS")
format_string = '%(asctime)s - %(lineno)d - %(levelname)s - %(message)s'
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.INFO)

def get_env(var):
    envvar = None
    if var.upper() in os.environ:
        envvar = os.environ[var.upper()]
    return envvar

client_id         = get_env('CLIENT-ID')
client_secret     = get_env('CLIENT-SECRET')
grant_type        = get_env('GRANT_TYPE')
base_url          = get_env('BASE_URL')
token_url         = get_env('TOKEN_URL')


app             = Flask(__name__)

def get_access_token():
    req = requests.post(url=token_url, data={"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type})
    if req.status_code != 200 and req.status_code != 201:
        logger.error("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
        raise AssertionError("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
    token = req.json()["access_token"]
    return token


@app.route('/<path:path>', methods=['POST'])
def meteringpoints(path):

    entities = request.get_json()
    # you might have to remove _ values form each entity

    logger.info("getting access token")
    token = get_access_token()
    logger.info("access token aquired")

    headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer {}".format(token)}
    for i, entity in enumerate(entities):
        #remove values starting with '_'
        req = requests.post(url = base_url + path, headers=headers, data=json.dumps(entity))
        if req.status_code != 200 and req.status_code != 201:
            logger.error("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
            raise AssertionError("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
        else:
            logger.info("Entity {} successfully sent".format(i))
    return "Pump successful"

if __name__ == '__main__':

    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
