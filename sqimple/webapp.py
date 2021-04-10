import flask
from subprocess import run
import logging


def make_app(args):
    app = flask.Flask(__name__, static_url_path="")

    @app.route("/")
    def index():
        return flask.render_template("index.html")


    @app.route("/query", methods=["POST"])
    def runquery():
        query = flask.request.get_data(as_text=True)
        logging.info(f'Running Query:\n{query}')
        result = args.run_query_func(query, args.database)
        return flask.jsonify(
            dict(result=result.stdout.decode(), error=result.stderr.decode())
        )

    return app
