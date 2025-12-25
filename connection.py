import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r'C:\oraclexe\app\oracle\product\11.2.0\server\bin')

connection_string = "dbmsthird/test@localhost:1521/XE"
connection = cx_Oracle.connect(connection_string)

cursor = connection.cursor()

cursor.execute("SELECT * from pizza")

result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
connection.close()
