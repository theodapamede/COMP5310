# 1. Clean the "data_variabilities" data set
# 2. Reload the "data_variabilities" dictionary into your database
# 3. Query the "Variability" table - which difference do you see?

# Reloading the data into a new variable
data_variabilities = list(csv.DictReader(open(''04at20gshortvariabilities.csv')))

# create function to clean data --> making non-readable data as np.nan

import warnings
import numpy as np
DEFAULT_VALUE = np.nan
def iter_clean(data, column_key, convert_function, default_value):
    for row in data:
        old_value = row[column_key]
        new_value = default_value
        try:
            new_value = convert_function(old_value)
        except (ValueError, TypeError):
            warnings.warn('Replacing {} with {} in column {}'.format(
                row[column_key], new_value, column_key))
        row[column_key] = new_value
        yield row

#source,oct04_flux,oct04_err,oct05_flux,oct05_err,apr06_flux,apr06_err
data_variabilities = list(iter_clean(data_variabilities, 'source', str, DEFAULT_VALUE))
data_variabilities = list(iter_clean(data_variabilities, 'oct04_flux', float, DEFAULT_VALUE))
data_variabilities = list(iter_clean(data_variabilities, 'oct04_err', float, DEFAULT_VALUE))
data_variabilities = list(iter_clean(data_variabilities, 'oct05_flux', float, DEFAULT_VALUE))
data_variabilities = list(iter_clean(data_variabilities, 'oct05_err', float, DEFAULT_VALUE))
data_variabilities = list(iter_clean(data_variabilities, 'apr06_flux', float, DEFAULT_VALUE))
data_variabilities = list(iter_clean(data_variabilities, 'apr06_err', float, DEFAULT_VALUE))

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
    
query_stmt = "SELECT * FROM Variabilities"
print(query_stmt)
pgquery (conn, query_stmt, None)
