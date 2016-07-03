# References for using JSONP
# https://gist.github.com/aisipos/1094140
# http://stackoverflow.com/questions/9348818/how-to-set-my-local-javascript-variable-as-a-json-data-on-remote-website/9348843#9348843
# http://stackoverflow.com/questions/9519209/how-do-i-set-up-jsonp

from flask import Flask, request, current_app
from functools import wraps
import json

# The main Flask app
app = Flask(__name__)


def jsonp(func):
    """ Wraps JSONified output for JSONP requests. """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get("callback", False)
        if callback:
            data = str(func(*args, **kwargs))
            content = str(callback) + "(" + data + ")"
            mimetype = "application/javascript"
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET"])
@jsonp  # Wrap with JSONP
def return_running_apps():

    # The content to dump to the client. Will probably be read from an
    # external server
    dataDict = open("data.json").read()

    # Dump it into JSON and return
    return json.dumps(dataDict)

if __name__ == "__main__":
    try:
        app.run()
    except:
        app.run(port=5001)
