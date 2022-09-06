import os
import time

from flask import Flask, abort, request, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)


@app.route('/')
def index():
    with open('WikiDist/templates/index.html', 'rb') as f:
        return f.read()


valid_chars = "abcdefghijklmnopqrstuvwxyz0123456789"


def filter_hidden(files):
    return [f for f in files if not f.startswith('.')]


def page_to_path(page):
    clean_page = ''.join([c for c in page if c in valid_chars])
    return 'WikiDist/pages/%s' % clean_page


def get_revisions(page):
    try:
        entries = filter_hidden(os.listdir(page_to_path(page)))
    except:
        abort(404)

    return sorted(map(int, entries))


def get_revision(page, timestamp):
    try:
        page_path = "%s/%i" % (page_to_path(page), timestamp)
        with open(page_path, 'r') as f:
            return jsonify(data=f.read(), title=page)
    except:
        abort(404)


@app.route('/pages')
def list_titles():
    return jsonify(titles=filter_hidden(os.listdir('WikiDist/pages')))


@app.route('/pages/<page>', methods=['GET'])
def list_revisions(page):
    try:
        return jsonify(revisions=get_revisions(page))
    except:
        abort(404)


@app.route('/pages/<page>/latest', methods=['GET'])
def get_latest_revision(page):
    latest = get_revisions(page)[-1]
    return get_revision(page, latest)


@app.route('/pages/<page>/<int:timestamp>', methods=['GET'])
def get_revision_at_time(page, timestamp):
    revisions = get_revisions(page)
    print(revisions)

    if timestamp < revisions[0]:
        abort(404)

    selected_revision = revisions[0]
    for page_timestamp in revisions:
        if page_timestamp <= timestamp:
            selected_revision = page_timestamp
        else:
            break

    return get_revision(page, selected_revision)


@app.route('/pages/<page>', methods=['POST'])
def write_page(page):
    new_revision = request.json['page']
    current_time = int(time.time())

    path = page_to_path(page)
    # Ensure directory exists
    try:
        os.stat(path)
    except:
        os.mkdir(path)

    page_path = "%s/%i" % (page_to_path(page), current_time)
    with open(page_path, 'wb') as f:
        f.write(new_revision)
        return "success"


if __name__ == '__main__':
    app.run(port=5003, debug=True, host="0.0.0.0")
