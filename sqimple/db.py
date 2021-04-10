import logging
from subprocess import run

def run_mysql_query(query, args):
    cmd = ['mysql', '--html']
    if args.username:
        cmd.extend(['-u', args.username])
    if args.password:
        cmd.append('--password={}'.format(args.password))
    if args.host:
        cmd.extend(['--host', args.host])
    if args.database:
        cmd.append(args.database)
    logging.debug(cmd)
    result = run(cmd, capture_output=True, input=query.encode())
    return result.stdout.decode(), result.stderr.decode()

def run_postgres_query(query, args):
    cmd = ['psql', '--html', args.database]
    logging.debug(cmd)
    if args.username:
        cmd.extend(['-U', args.username])
    if args.host:
        cmd.extend(['-h', args.host])
    result = run(cmd, capture_output=True, input=query.encode())
    return result.stdout.decode(), result.stderr.decode()

def run_sqlite_query(query, args):
    cmd = ["sqlite3", "-header", "-html", args.database]
    logging.debug(cmd)
    result = run(cmd, capture_output=True, input=query.encode())
    # while the other dbs wrap their html output in a <table> element, sqlite
    # does not, so we'll add it ourselves here
    return (
        '<table>' + result.stdout.decode() + '</table>',
        result.stderr.decode()
    )
