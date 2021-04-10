import argparse
from sqimple import db


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    parser.add_argument(
        "-v", action="count", help="be verbose (enable query logging)", default=0
    )
    parser.add_argument(
        "--debug", action="store_true", help="run webserver in debug mode"
    )

    subparsers = parser.add_subparsers(
        title="subcommands",
        description="database backend to use",
        help='One of {sqlite,mysql,pg}',
        required=True,
        dest="subcommand",
        metavar='subcommand',
    )

    sqlite_parser = subparsers.add_parser("sqlite")
    sqlite_parser.add_argument(
        "database",
        nargs="?",
        default=":memory:",
        help="SQLite database to interact with. Defaults to in-memory db.",
    )
    sqlite_parser.set_defaults(run_query_func=db.run_sqlite_query)

    mysql_parser = subparsers.add_parser("mysql")
    mysql_parser.add_argument('database') # TODO: actually optional
    mysql_parser.set_defaults(run_query_func=db.run_mysql_query)

    pg_parser = subparsers.add_parser("pg", aliases=["postgres", "postgresql"])
    pg_parser.add_argument('database')
    pg_parser.set_defaults(run_query_func=db.run_postgres_query)

    return parser.parse_args()
