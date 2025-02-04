# import os
# os.system('python.exe main_window.py')
# os.system('python.exe server/backendServer.py')

import mysql.connector
table_name = "clientData"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database = "verifiedclients",
)

c = db.cursor()
c.execute("CREATE TABLE `clientData` ("
          "`hash` VARCHAR(30), `platform` VARCHAR(30), `platform-release` VARCHAR(30), "
          "`platform-version` VARCHAR(30), `architecture` VARCHAR(30), `processor` VARCHAR(30), `hostname` VARCHAR(30), `ram` VARCHAR(30))")




# c.execute("DROP TABLE `clientData`")