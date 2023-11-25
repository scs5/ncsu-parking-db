import sqlite3 as sql

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


if __name__ == '__main__':
    drop_tables()