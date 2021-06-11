import cx_Oracle

con = cx_Oracle.connect('mydb/mydb@localhost:1521/xe')
cursor = con.cursor()

cursor.execute('select * from linkedin')

for companyName, company, websiteName, phoneNumber, companySize, queryVal in cursor:
    print("Name:", companyName)
    print("LinkedIn Page:", company)
    print("Website:", websiteName)
    print("Phone Number:", phoneNumber)
    print("Company Size:", companySize)
    print("Domain:", queryVal)
    print()

if cursor:
    cursor.close()
if con:
    con.close()