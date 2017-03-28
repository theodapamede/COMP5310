# import csv module to read the csv file
import csv

# import pprint module (don't know why)
import pprint

# import psycopg2 module to connect to postgresql database
import psycopg2
try: 
    conn = psycopg2.connect(database='tdap2572', user='tdap2572', password='470239731')
    print('connected')
except Exception as e:
    print("I am unable to connect to the database")
    print(e)
# it should output: "connected", if correct

# create pgexec function
# dedicated function for executing an arbitrary SQL statement,
# where we do not expect any results
# this will automatically commit our SQL statements,
# as well as rollback if there was any error
def pgexec( conn, sqlcmd, args, msg ):
   """ utility function to execute some SQL statement
       can take optional arguments to fill in (dictionary)
       error and transaction handling built-in """
   retval = False
   with conn:
      with conn.cursor() as cur:
         try:
            if args is None:
               cur.execute(sqlcmd)
            else:
               cur.execute(sqlcmd, args)
            print("success: " + msg)
            retval = True
         except Exception as e:
            print("db error: ")
            print(e)
   return retval

# create "data_variabilites" as variable to make table "variabilities"
data_variabilities = list(csv.DictReader(open('04at20gshortvariabilities.csv')))

# LOADING DATA AND CREATING TABLES
# use VARCHAR as data type, and set source as the PRIMARY KEY
variabilities_schema = """CREATE TABLE IF NOT EXISTS Variabilities (
                         source VARCHAR PRIMARY KEY,
                         oct04_flux VARCHAR,
                         oct04_err VARCHAR,
                         oct05_flux VARCHAR,
                         oct05_err VARCHAR,
                         apr06_flux VARCHAR,
                         apr06_err VARCHAR
                   )"""
pgexec (conn, variabilities_schema, None, "Create Table Variabilities")

insert_stmt = """INSERT INTO Variabilities(source,oct04_flux,oct04_err,oct05_flux,oct05_err,apr06_flux,apr06_err)
                      VALUES (%(source)s, %(oct04_flux)s, %(oct04_err)s, %(oct05_flux)s, %(oct05_err)s, %(apr06_flux)s, %(apr06_err)s)"""
for row in data_variabilities:
    pgexec (conn, insert_stmt, row, "row inserted")

# PGQUERY function to print out the table results
def pgquery( conn, sqlcmd, args ):
   """ utility function to execute some SQL query statement
       can take optional arguments to fill in (dictionary)
       will print out on screen the result set of the query
       error and transaction handling built-in """
   retval = False
   with conn:
      with conn.cursor() as cur:
         try:
            if args is None:
                cur.execute(sqlcmd)
            else:
                cur.execute(sqlcmd, args)
            for record in cur:
                print(record)
            retval = True
         except Exception as e:
            print("db read error: ")
            print(e)
   return retval

# check content of Frequency table
query_stmt = "SELECT * FROM Frequency"
print(query_stmt)
pgquery (conn, query_stmt, None)

# cleanup...   Needed already?  Better not now... 
# But keep in mind to close comnnection eventually!
# conn.close()
