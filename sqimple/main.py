import logging

import flask
import waitress

from sqimple.webapp import make_app
from sqimple.cli import get_args


def main():
    args = get_args()

    if args.v > 1:
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

    logging.debug('args:')
    logging.debug(args)
    app = make_app(args)

    print()
    print("   Starting Up!")
    print()
    print("   Visit http://localhost:{} in your browser.".format(args.port))
    print("   Press Ctrl-C to exit.".format(args.port))
    print()

    if args.debug:
        app.run(debug=True, port=args.port, host="127.0.0.1")
    else:
        waitress.serve(app, port=args.port, host="127.0.0.1")


if __name__ == "__main__":
    main()
