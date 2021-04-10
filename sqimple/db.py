from subprocess import run

def run_mysql_query(query, database):
    raise NotImplementedError

def run_postgres_query(query, database):
    raise NotImplementedError

def run_sqlite_query(query, database):
    cmd = ["sqlite3", "-header", "-html", database, query]
    return run(cmd, capture_output=True)
