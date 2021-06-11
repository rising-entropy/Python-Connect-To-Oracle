import cx_Oracle

con = cx_Oracle.connect('mydb/mydb@localhost:1521/xe')
cursor = con.cursor()

cursor.execute('insert into linkedin values(\'un\',\'dos\', \'tres\', \'quatro\', \'wowowo\')')
con.commit()

if cursor:
    cursor.close()
if con:
    con.close()