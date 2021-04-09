import flask
from subprocess import run

app = flask.Flask(__name__, static_url_path="")

DATABASE = ":memory:"


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/query", methods=["POST"])
def runquery():
    query = flask.request.get_data(as_text=True)
    result = run(["sqlite3", "-header", "-html", DATABASE, query], capture_output=True)
    return flask.jsonify(
        dict(result=result.stdout.decode(), error=result.stderr.decode())
    )


def main():
    global DATABASE
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "sqlite_db",
        nargs="?",
        help="SQLite database to interact with. Defaults to in-memory db.",
    )
    args = parser.parse_args()

    if args.sqlite_db:
        DATABASE = args.sqlite_db

    app.run(debug=True)


if __name__ == "__main__":
    main()
