import argparse
import logging
from subprocess import run

import flask
import waitress

app = flask.Flask(__name__, static_url_path="")

DATABASE = ":memory:"


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/query", methods=["POST"])
def runquery():
    query = flask.request.get_data(as_text=True)
    logging.info(f'Running Query:\n{query}')
    cmd = ["sqlite3", "-header", "-html", DATABASE, query]
    logging.debug(cmd)
    result = run(cmd, capture_output=True)
    return flask.jsonify(
        dict(result=result.stdout.decode(), error=result.stderr.decode())
    )

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sqlite_db",
        nargs="?",
        help="SQLite database to interact with. Defaults to in-memory db.",
    )
    parser.add_argument('-p', '--port', default=5000)
    parser.add_argument('-v', action='count', help='be verbose (enable query logging)', default=0)
    return parser.parse_args()

def main():
    global DATABASE
    args = get_args()

    if args.v >= 2:
        level = logging.DEBUG
    elif args.v > 0:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
        format="[sqimple %(asctime)s %(levelname)s]%(message)s",
    )

    if args.sqlite_db:
        DATABASE = args.sqlite_db

    print()
    print("   Starting Up!")
    print()
    print("   Visit http://localhost:{} in your browser.".format(args.port))
    print("   Press Ctrl-C to exit.".format(args.port))
    print()
    waitress.serve(app, port=args.port, host="127.0.0.1")


if __name__ == "__main__":
    main()
