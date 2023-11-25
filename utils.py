import pandas as pd
import sqlite3 as sql
import datetime
import re

def create_tables():
    # Connect to database
    conn = sql.connect('parking.db')
    curs = conn.cursor()

    curs.execute("""DROP TABLE IF EXISTS tDrivers;""")
    curs.execute("""CREATE TABLE tDrivers (
        univID_phonenumber INTEGER PRIMARY KEY CHECK (LENGTH(CAST(univID_phonenumber AS TEXT)) IN (9, 10)),
        name TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('S', 'E', 'V'))
        );""")

    curs.execute("""DROP TABLE IF EXISTS tVehicles;""")
    curs.execute("""CREATE TABLE tVehicles (
        license_number TEXT PRIMARY KEY,
        model TEXT NOT NULL,
        color TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        year INTEGER NOT NULL
        );""")

    curs.execute("""DROP TABLE IF EXISTS tDrive;""")
    curs.execute("""CREATE TABLE tDrive (
        license_number TEXT,
        univID_phonenumber INTEGER,
        PRIMARY KEY (univID_phonenumber, license_number),
        FOREIGN KEY (univID_phonenumber) REFERENCES tDrivers (univID_phonenumber) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (license_number) REFERENCES tVehicles (license_number) ON UPDATE CASCADE ON DELETE CASCADE
        );""")

    curs.execute("""DROP TABLE IF EXISTS tPermits;""")
    curs.execute("""CREATE TABLE tPermits (
        permitID INTEGER PRIMARY KEY,
        permit_type TEXT NOT NULL CHECK (permit_type IN ('Residential', 'Commuter', 'Peak Hours', 'Special Event', 'Park & Ride')),
        space_type TEXT NOT NULL CHECK (space_type IN ('Electric', 'Handicap', 'Compact Car', 'Regular')),
        start_date DATE,
        expiration_date DATE,
        expiration_time TIME
        );""")

    curs.execute("""DROP TABLE IF EXISTS tAreAssigned;""")
    curs.execute("""CREATE TABLE tAreAssigned (
        univID_phonenumber INTEGER,
        permitID INTEGER,
        PRIMARY KEY (univID_phonenumber, permitID),
        FOREIGN KEY (univID_phonenumber) REFERENCES tDrivers (univID_phonenumber) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (permitID) REFERENCES tPermits (permitID) ON UPDATE CASCADE ON DELETE CASCADE
        );""")

    curs.execute("""DROP TABLE IF EXISTS tAreAssociatedWith;""")
    curs.execute("""CREATE TABLE tAreAssociatedWith (
        license_number TEXT,
        permitID INTEGER,
        PRIMARY KEY (license_number, permitID),
        FOREIGN KEY (license_number) REFERENCES tVehicles (license_number) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (permitID) REFERENCES tPermits (permitID) ON UPDATE CASCADE ON DELETE CASCADE
        );""")

    curs.execute("""DROP TABLE IF EXISTS tLots;""")
    curs.execute("""CREATE TABLE tLots (
        lot_name TEXT PRIMARY KEY,
        address TEXT NOT NULL,
        UNIQUE (address)
        );""")

    curs.execute("""DROP TABLE IF EXISTS tZones;""")
    curs.execute("""CREATE TABLE tZones (
        lot_name TEXT,
        zoneID TEXT,
        PRIMARY KEY (lot_name, zoneID),
        FOREIGN KEY (lot_name) REFERENCES tLots (lot_name) ON UPDATE CASCADE ON DELETE CASCADE
        );""")

    curs.execute("""DROP TABLE IF EXISTS tAllowsDriverToParkIn;""")
    curs.execute("""CREATE TABLE tAllowsDriverToParkIn (
        permitID INTEGER,
        zoneID TEXT,
        lot_name TEXT,
        PRIMARY KEY (permitID, zoneID, lot_name),
        FOREIGN KEY (permitID) REFERENCES tPermits (permitID) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (lot_name, zoneID) REFERENCES tZones (lot_name, zoneID) ON UPDATE CASCADE ON DELETE CASCADE
        );""")

    curs.execute("""DROP TABLE IF EXISTS tSpaces;""")
    curs.execute("""CREATE TABLE tSpaces (
        lot_name TEXT,
        zoneID TEXT,
        space_number INTEGER,
        space_type TEXT CHECK (space_type IN ('Electric', 'Handicap', 'Compact Car', 'Regular')),
        availability TEXT CHECK(availability IN ('Available', 'Unavailable')),
        PRIMARY KEY (space_number, zoneID, lot_name),
        FOREIGN KEY (lot_name, zoneID) REFERENCES tZones (lot_name, zoneID) ON UPDATE CASCADE ON DELETE CASCADE
        );""")

    curs.execute("""DROP TABLE IF EXISTS tCitations;""")
    curs.execute("""CREATE TABLE tCitations (
        citation_number INTEGER PRIMARY KEY,
        category TEXT NOT NULL CHECK (category IN ('Invalid Permit', 'Expired Permit', 'No Permit')),
        citation_date DATE NOT NULL,
        citation_time TIME NOT NULL,
        fee INTEGER NOT NULL,
        payment_status TEXT DEFAULT 'unpaid' NOT NULL CHECK (payment_status IN ('Paid', 'Unpaid', 'Appealed'))
        );""")

    curs.execute("""DROP TABLE IF EXISTS tAreTicketedTo;""")
    curs.execute("""CREATE TABLE tAreTicketedTo (
        license_number TEXT,
        citation_number INTEGER,
        PRIMARY KEY (license_number, citation_number),
        FOREIGN KEY (license_number) REFERENCES tVehicles (license_number) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (citation_number) REFERENCES tCitations (citation_number) ON UPDATE CASCADE ON DELETE CASCADE
        );""")

    curs.execute("""DROP TABLE IF EXISTS tAreIssuedWithin;""")
    curs.execute("""CREATE TABLE tAreIssuedWithin (
        lot_name TEXT,
        citation_number INTEGER,
        PRIMARY KEY (lot_name, citation_number),
        FOREIGN KEY (lot_name) REFERENCES tLots (lot_name) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (citation_number) REFERENCES tCitations (citation_number) ON UPDATE CASCADE ON DELETE CASCADE
        );""")
    
    conn.commit()
    conn.close()


def load(table_name, df, option=0, type="row", demo=False):
    """This function loads data from df into the table called table_name.
    For proper use, column order in df should match the order of attributes
    listed in the table's create statement (found in create_tables.py).
    df should be a dataframe or a list. If type is 'row', it will expect a list
    (a single insertion). If type is 'bulk', it will expect a dataframe (multiple insertions)"""

    # Connect to database
    conn = sql.connect('parking.db')
    curs = conn.cursor()

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

    # Close connection
    conn.close()


def drop_tables():
    conn = sql.connect('parking.db')
    curs = conn.cursor()

    # Drop tables in reverse order to avoid foreign key constraints
    curs.execute("""DROP TABLE IF EXISTS tAreIssuedWithin;""")
    curs.execute("""DROP TABLE IF EXISTS tAreTicketedTo;""")
    curs.execute("""DROP TABLE IF EXISTS tCitations;""")
    curs.execute("""DROP TABLE IF EXISTS tSpaces;""")
    curs.execute("""DROP TABLE IF EXISTS tAllowsDriverToParkIn;""")
    curs.execute("""DROP TABLE IF EXISTS tZones;""")
    curs.execute("""DROP TABLE IF EXISTS tLots;""")
    curs.execute("""DROP TABLE IF EXISTS tAreAssociatedWith;""")
    curs.execute("""DROP TABLE IF EXISTS tAreAssigned;""")
    curs.execute("""DROP TABLE IF EXISTS tPermits;""")
    curs.execute("""DROP TABLE IF EXISTS tDrive;""")
    curs.execute("""DROP TABLE IF EXISTS tVehicles;""")
    curs.execute("""DROP TABLE IF EXISTS tDrivers;""")

    conn.commit()
    conn.close()


def load_demo_data():
    # Reset database
    drop_tables()
    create_tables()

    # Load driver data
    driver_data = pd.read_csv('./demo-data/drivers.csv')
    load('tDrivers', driver_data, option = 1, type = "bulk", demo=True)

    # Load parking lot data
    lot_data = pd.read_csv('./demo-data/parkinglots.csv')
    load('tLots', lot_data, option = 1, type = "bulk", demo=True)

    # Load vehicle data
    vehicle_data = pd.read_csv('./demo-data/vehicles.csv')
    load('tVehicles', vehicle_data, option = 1, type = "bulk", demo=True)

    # Load drive relation data
    drive_data = pd.DataFrame({
        'license_number': vehicle_data['license_number'],
        'univID_phonenumber': driver_data['univID_phonenumber']
    })
    load('tDrive', drive_data, option = 1, type = "bulk", demo=True)

    # Load permit data
    permit_data = pd.read_csv('./demo-data/permits.csv')
    assigned_to_data = pd.DataFrame({
        'univID_phonenumber': driver_data['univID_phonenumber'],
        'permitID': range(1, 7)
    })
    vehicle_data.drop(vehicle_data.index[-1], inplace=True)
    associated_with_data = pd.DataFrame({
        'license_number': vehicle_data['license_number'],
        'permitID': range(1, 7)
    })
    updated_permit_data = permit_data.drop(['permitID', 'zoneID', 'univID_phonenumber'], axis=1)
    print(updated_permit_data)
    load('tPermits', updated_permit_data, option = 1, type = "bulk", demo=True)
    load('tAreAssociatedWith', associated_with_data, option = 1, type = "bulk", demo=True)
    load('tAreAssigned', assigned_to_data, option = 0, type = "bulk", demo=True)

    # Load zone data
    zone_data = pd.DataFrame({
        'lot_name': ['Poulton Deck', 'Poulton Deck', 'Partners Way Deck',   # made this up -- not included in demo data
                     'Dan Allen Parking Deck', 'Poulton Deck', 'Partners Way Deck'],
        'zoneID': permit_data['zoneID']
    })
    load('tZones', zone_data, option = 1, type = "bulk", demo=True)

    # Load permit-zone relation data
    allows_drivers_data = pd.DataFrame({
        'permitID': [5, 2, 3, 4, 1, 6],
        'zoneID': zone_data['zoneID'],
        'lot_name': zone_data['lot_name']
    })
    print(allows_drivers_data)
    load('tAllowsDriverToParkIn', allows_drivers_data, option = 0, type = "bulk", demo=True)

    # Load citation data
    citation_data = pd.read_csv('./demo-data/citations.csv')
    ticketed_to_data = citation_data[['license_number', 'citation_number']]
    issued_within_data = citation_data[['lot_name', 'citation_number']]
    citation_data = citation_data[['citation_number', 'category', 'citation_date', 'citation_time', 'fee', 'payment_status']]
    citation_data = citation_data.drop('citation_number', axis=1)
    load('tCitations', citation_data, option = 0, type = "bulk", demo=True)
    load('tAreTicketedTo', ticketed_to_data, option = 1, type = "bulk", demo=True)
    load('tAreIssuedWithin', issued_within_data, option = 1, type = "bulk", demo=True)


def is_valid_date(date_string):
    """ Determine whether a date is valid. """

    # Regular expression pattern for "YYYY-MM-DD" format
    if not date_string:
        return False
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    # Check if the date_string matches the pattern
    if not re.match(pattern, date_string):
        return False
    
    # Parse the date using datetime.strptime and check if it's a valid calendar date
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    

def is_valid_time(time_string):
    """ Determine whether a time is valid. """
    
    # Regular expression pattern for "HH:MM:SS" format
    if not time_string:
        return False
    pattern = r'^\d{2}:\d{2}:\d{2}$'
    
    # Check if the time_string matches the pattern
    if not re.match(pattern, time_string):
        return False
    
    # Parse the time using datetime.strptime and check if it's a valid time
    try:
        datetime.datetime.strptime(time_string, "%H:%M:%S")
        return True
    except ValueError:
        return False