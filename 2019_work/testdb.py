import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'

                                'Server=localhost\SQLEXPRESS;'

                                'Database=ffl;'

                                'Trusted_Connection=yes;')

cursor = connection.cursor()
cursor.execute("SELECT * FROM dbo.test")
while 1:
    row = cursor.fetchone()
    if not row:
        break
    print(row)
cursor.execute("insert into dbo.test values (?,?) ",[1,2])
connection.commit()   
connection.close()