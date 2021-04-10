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

    mysql_parser = subparsers.add_parser("mysql", conflict_handler='resolve')
    mysql_parser.add_argument('database', nargs='?', help='Database to connect to')
    mysql_parser.add_argument('-u', '--username')
    mysql_parser.add_argument('-p', '--password')
    mysql_parser.add_argument('-h', '--host')
    mysql_parser.set_defaults(run_query_func=db.run_mysql_query)

    #  -h, --host=HOSTNAME      database server host or socket directory (default: "local socket")
    #  -p, --port=PORT          database server port (default: "5432")
    #  -U, --username=USERNAME  database user name (default: "zach")
    #  -w, --no-password        never prompt for password
    #  -W, --password           force password prompt (should happen automatically)

    pg_parser = subparsers.add_parser("pg", aliases=["postgres", "postgresql"], conflict_handler='resolve')
    pg_parser.add_argument('-d', '--database')
    pg_parser.add_argument('-U', '--username')
    pg_parser.add_argument('-h', '--host')
    pg_parser.set_defaults(run_query_func=db.run_postgres_query)

    return parser.parse_args()
