
import pandas as pd 
import mysql.connector as mys 

print ("Halo kawan")

mydb = mys.connect(
  host="localhost",
  user="root",
  password="database_ku",
  database="PortFolioProject_DataCovid"
)

data = pd.read_excel ("/Users/eveambergoodmon/Documents/Belajar Python/Data Analyst /Covid Data.xlsx")

mycursor = mydb.cursor()

# Adapt the table structure based on your Excel data
mycursor.execute(
    '''CREATE TABLE IF NOT EXISTS Data_CovidDeath (ISO_Code VARCHAR(50), Benua VARCHAR (100), 
    loc VARCHAR (100), tanggal DATE, populasi int, total_case int, new_cases int, new cases_smoothed, total_death int, 
    new_death int)'''
    )
mydb.commit()

'''
for index, row in data.iterrows():
  sql = "INSERT INTO Data_CovidDeath (column1, column2, ...) VALUES (%s, %s, ...)"
  val = tuple(row)
  mycursor.execute(sql, val)

mydb.commit()
'''


