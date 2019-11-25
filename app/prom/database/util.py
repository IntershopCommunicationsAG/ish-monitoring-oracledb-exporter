import logging
import socket

from cx_Oracle import connect, makedsn, DatabaseError, InterfaceError
from flask import current_app as app

LOGGER = logging.getLogger(__name__)


def is_port_open():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((app.config["SERVER"], int(app.config["PORT"])))
        s.shutdown(2)
        return True
    except:
        return False


def get_connection():
    server = app.config["SERVER"]
    port = app.config["PORT"]
    service = app.config["SERVICE"]
    user = app.config["USERNAME"]
    password = app.config["PASSWORD"]
    try:
        conn = connect(user, password, makedsn(server, port, service))
    except DatabaseError:
        raise InterfaceError
    return conn


def makeDictFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow


def get_query_result(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.rowfactory = makeDictFactory(cursor)
        result = cursor.fetchall()
        for row in result:
            yield row
    except DatabaseError as e:
        LOGGER.error("Query: %s has error: %s", query, str(e))
