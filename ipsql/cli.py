""" Command line interface entry point."""

import getpass
import optparse

import psycopg2

from ipsql.shell import Shell

def get_parser():
    parser = optparse.OptionParser(add_help_option=False)
    parser.add_option(
        "-c", "--command",
        help="run only single command (SQL or internal) and exit")
    parser.add_option(
        "-h", "--host",
        help="database server host or socket directory")
    parser.add_option(
        "-p", "--port",
        help="database server port")
    parser.add_option(
        "-d", "--dbname",
        help="database name to connect to")
    parser.add_option(
        "-U", "--username",
        help="database user name")
    return parser

def main():
    parser = get_parser()
    options, args = parser.parse_args()

    # TODO: Better handling data type conversion errors.
    host = options.host if options.host else "localhost"
    port = int(options.port) if options.port else 5432
    username = options.username if options.username else getpass.getuser()
    dbname = options.dbname if options.dbname else username

    connection = psycopg2.connect(
        database=dbname,
        user=username,
        host=host,
        port=port)

    shell = Shell(connection)
    shell.run()
