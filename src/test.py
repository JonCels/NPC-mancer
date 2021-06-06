import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jDAN0921",
    auth_plugin='mysql_native_password',
    database='npc_mancer_db'
)

mycursor = db.cursor()
mycursor.execute("select * from races")
races = []
for race in mycursor:
    races.append(race);