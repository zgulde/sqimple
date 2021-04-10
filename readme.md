# Sqimple

Simple SQL Web Interface for sqlite, mysql, and postgres databases.

Intended to be a step between the DBMS' interactive command line interface and a
fully-featured SQL GUI client.

## Usage

```
python -m pip install sqimple
```

One of:

- sqlite

    ```
    sqimple sqlite mydb.sqlite
    ```

- mysql

    ```
    sqimple mysql -u someusername -p mypassword --host db.example.com some_database
    ```

- postgres

    ```
    sqimple pg -U username -d database
    ```

and then visit http://localhost:5000 in your browser.

See the help or subcommand help for more options:

```
sqimple --help
sqimple mysql --help
```

## Notes

- no state is persisted between query executions
- for postgres passwords, use a `~/.pgpass` file
- when saving the query to a file, if the specified filename already exists it
  will be overridden
