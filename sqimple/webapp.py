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
        out, err = args.run_query_func(query, args)
        return flask.jsonify(dict(result=out, error=err))

    @app.route("/save/<filename>", methods=["POST"])
    def savefile(filename):
        query = flask.request.get_data(as_text=True)
        with open(filename, 'w+') as f:
            f.write(query)
        return f'{filename} saved!'

    return app
