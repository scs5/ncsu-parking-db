import pandas as pd
import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()
import numpy as np

# sql = """select * from pragma_table_info('tVehicles');"""
#
# curs.execute(sql)
# print(curs.fetchall())
def load(table_name, df, option=0, type="row", demo=False):
    """This function loads data from df into the table called table_name.
    For proper use, column order in df should match the order of attributes
    listed in the table's create statement (found in create_tables.py).
    df should be a dataframe or a list. If type is 'row', it will expect a list
    (a single insertion). If type is 'bulk', it will expect a dataframe (multiple insertions)"""

    # Get the list of column names in the table
    curs.execute("PRAGMA table_info(" + table_name + ");")
    table_info = curs.fetchall()
    cols = [col[1] for col in table_info]

    # Auto-increment these for demo data
    if (demo):
        if table_name == 'tPermits':
            cols.remove('permitID')
        if table_name == 'tCitations':
            cols.remove('citation_number')

    print('COLS',cols)
    # Generate the SQL statement for inserting into the remaining columns
    sql_insert = "INSERT INTO " + table_name + " (" + ", ".join(cols) + ") VALUES (" + ", ".join(['?'] * len(cols)) + ");"

    # Set foreign key constraints
    curs.execute("PRAGMA foreign_keys = 1")

    # If the type is 'row', convert the input data to a DataFrame
    if type == "row":
        df_new = pd.DataFrame(columns=cols)
        print('LOADING',df_new)
        df_new.loc[0] = df
        df = df_new
    curs.execute("BEGIN TRANSACTION;")

    # Insert the data into the table
    if option == 0:
        for row in df.values:
            row = row.tolist()
            print('ROW:',row)
            try:
                print(sql_insert)
                curs.execute(sql_insert,row)
            except:
                print('Invalid data provided: ',row)
            curs.execute("COMMIT;")
            print('Change committed.')
    elif option == 1:  # if one doesn't work, the whole thing fails
        try:
            for row in df.values:
                row = row.tolist()
                curs.execute(sql_insert, row)
            curs.execute("COMMIT;")
        except:
            print('failure')
            curs.execute("ROLLBACK;")





# df = pd.DataFrame()
# df['univID_phonenumber'] = ['123456789','234567891']
# df['name'] = ['John C','Casey M']
# df['status'] = ['S','F']
# # for row in df.values:
# #     print(row)
# load('tDrivers',df,option = 1,type = "bulk")
# curs.execute("SELECT * FROM tDrivers;")
# print(curs.fetchall())
#
# df2 = pd.DataFrame()
# df2['license_number'] = ['abc123','def456']
# df2['model'] = ['Crosstreck','Fiesta']
# df2['color'] = ['Blue','Black']
# df2['manufacturer'] = ['Subaru', 'Ford']
# df2['year'] = [2022,2016]
# for row in df2.values:
#     print(row)
# load('tVehicles',df2,option = 1,type = "bulk")
#
# curs.execute("SELECT * FROM tVehicles;")
# print(curs.fetchall())
#
#
# df3 = pd.DataFrame()
# df3['license_number'] = ['abc123','def456']
# df3['univID_phonenumber'] = ['123456789','234567891']
# # for row in df3.values:
# #     print(row)
# load('tDrive',df3,option = 1,type = "bulk")
#
# curs.execute("SELECT * FROM tDrive;")
# print(curs.fetchall())
# conn.close()
