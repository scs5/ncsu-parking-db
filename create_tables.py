import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()

def create_tables():
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

if __name__ == '__main__':
    create_tables()
    conn.close()
