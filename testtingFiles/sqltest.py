import mysql.connector
from mysql.connector import Error
import requests
import json

def create_database_connection(databaseName, session):
    databaseConnection = None
    try:
        with session:
            if databaseName == "verifiedclients":
                databaseConnection = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    passwd = "0324",
                    port = "3305",
                    database = databaseName,
                    auth_plugin = "mysql_native_password"
                )
                print("Session created")
                return databaseConnection

    except Error as err:
        print(err)



def formatDatabaseQuery(data, table_name, hash):
    # SANITIZE DATA FIRST!!!!!!!!!!!!!!!!

    sysdata = data['systemData']

    query = """
    INSERT INTO %s VALUES (
    "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"
    );

    """ % (table_name, hash, sysdata['platform'], sysdata['platform-release'], sysdata['platform-version'], sysdata['architecture'], sysdata['processor'], sysdata['hostname'], sysdata['ram'])

    return query


def execute_query(query, databaseConnection, session):
    with session:
        cursor = databaseConnection.cursor()
        try:
            # cursor.execute('SET GLOBAL max_allowed_packet=67108864')
            cursor.execute(query)
            databaseConnection.commit()
            print("Data written to database")

        except Error as err:
            print(err)





def start():
    data = ({'systemData': {'platform': 'Windows', 'platform-release': '10', 'platform-version': '10.0.22621', 'architecture': 'AMD64', 'hostname': 'PRELUDE-1', 'processor': 'AMD64 Family 23 Model 96 Stepping 1, AuthenticAMD', 'ram': '31 GB'}})
    table_name = "clientData"
    hash = "E66-f03276613eb5033debbbd18d11139be6f77e9596"
    with requests.Session() as session:
        databaseConnection = create_database_connection(databaseName="verifiedclients", session=session)
        query = formatDatabaseQuery(data, table_name, hash)
        execute_query(query, databaseConnection, session)
            


start()