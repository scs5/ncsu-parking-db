# This page is meant to handle any queries that involve reporting out some output.
# Tasks and Operations: Reports
import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()

# This provides an overall citation report for any citations in the system
def generateCompleteReport():
    try:
        curs.execute("SELECT citation_number, citation_date, citation_time, category, fee, payment_status FROM tCitations")
        citations = curs.fetchall()
       
        # If there are no citations in the database, we print a message and return out of the method
        if not citations:
            print("No citations found in the database.")
            return
        
        # It prints the citation report with --> citation number, citation date, citation time, category, fee, payment status
        print("\nCitation Report:")
        for citation in citations:
            citation_number, citation_date, citation_time, category, fee, payment_status = citation
            print(f"Citation Number: {citation_number}")
            print(f"Citation Date: {citation_date}")
            print(f"Citation Time: {citation_time}")
            print(f"Category: {category}")
            print(f"Fee: {fee}")
            print(f"Payment Status: {payment_status}")
            print("")
    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print("Error generating citation report.")
        print(f"SQLite error: {e}")

# Generates the citations that happened within the range of startDate -> endDate
def generateCitationsInRange(startDate: str, endDate: str):
    sql = "SELECT DISTINCT lot_name FROM tLots;"
    curs.execute(sql)
    lots = [l[0] for l in curs.fetchall()]
    if len(lots)==0:
        print('No lots found.')
        return
    counts = []
    for lotName in lots:
        try:
            # Making sure the user enters all required fields
            if startDate == "" or endDate == "" or lotName == "":
                print("You must provide a start and end date along with a lot name.")
                return
            count_query = "SELECT num from (SELECT lot_name, COUNT(*) AS num FROM tCitations NATURAL JOIN tAreIssuedWithin WHERE citation_date BETWEEN ? AND ? GROUP BY lot_name) WHERE lot_name == ?;"
            curs.execute(count_query, (startDate, endDate, lotName))
            result = curs.fetchall()
            if len(result) == 0:
                counts.append(0)
                print('\n'+lotName + ' : 0')
            else:
                
                total = result[0][0]
                counts.append(total)
                print(f"\n"+lotName+" : "+str(total))

        except sql.Error as e:
            # If an error happens we print the message (useful for debugging the code)
            print(f"Error generating total citations report: {e}")
    #print(lots,counts)
    return


# List the zones in each lot as a tuple pair
def listZonesForEachLot():
    try:
        curs.execute("SELECT lot_name, zoneID FROM tZones")
        zone_lot_pairs = curs.fetchall()

        # Traverse the lots and zones in the pairs and print them out as a tuple
        print()
        for lot, zone in zone_lot_pairs:
            print(f"Lot: {lot}, Lot: {zone}")

    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print(f"Error listing zones for lots: {e}")
    
# Checking how many cars are currently in violation
# A car is in violation if the payment status == 'Unpaid'
# In the demo date they also gave us payment status == 'DUE' so that is also listed as an option
def carsCurrentlyInViolation():
    try:
        curs.execute("SELECT COUNT(*) FROM tCitations WHERE payment_status = 'Unpaid' OR payment_status = 'DUE'")
        cars_in_violation_count = curs.fetchall()[0][0]

        print("\nNumber of cars currently in violation:", cars_in_violation_count)

    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print("Error counting cars in violation")
    
# Reporting what employees can park in a specific zone
def employeesWithPermitInZone(zoneID: str):
    try:
        # Making sure the user provided us with a zoneID
        if zoneID == "":
            print("You must provide a zoneID.")
            return
        # Performing the required joins to get from tZones to tDrivers in order to see which Employees can park in a given zone
        # We have to join with tAreAssigned, tPermits, & tAllowsDriverToParkIn
        curs.execute("""
            SELECT tDrivers.*
            FROM tDrivers
            JOIN tAreAssigned ON tDrivers.univID_phonenumber = tAreAssigned.univID_phonenumber
            JOIN tPermits ON tAreAssigned.permitID = tPermits.permitID
            JOIN tAllowsDriverToParkIn ON tPermits.permitID = tAllowsDriverToParkIn.permitID
            WHERE tAllowsDriverToParkIn.zoneID = ? AND tDrivers.status = 'E'
        """, (zoneID,))

        # Storing all the employee information
        employee_info = curs.fetchall()
        # Going through each employee that is able to park in this zone and printing their univID_phonenumber, name and status (attributes of a driver)
        if employee_info:
            print()
            for row in employee_info:
                univID_phonenumber, name, status = row
                print(f"University ID/Phone Number: {univID_phonenumber}")
                print(f"Name: {name}")
                print(f"Status: {status}")
                print()
        else:
            # Handling the case where there are no drivers that are able to park in the given zone
            print(f"No employees found with permits in zone: {zoneID}")

    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print(f"Error getting employees with permits")
    
# Printing all the permit information for a driver given their university ID or phone number
def permitInfoGivenIdNumber(univID_phonenumber: str):
    try:
        # Making sure the user provided us with a university ID or phone number
        if univID_phonenumber == "":
            print("You must provide us with a university ID or phone number.")
            return
        # curs.execute("SELECT * FROM tPermits WHERE univID_phonenumber = ?;", (univID_phonenumber))
        curs.execute("""
            SELECT tPermits.*
            FROM tPermits
            JOIN tAreAssigned ON tPermits.permitID = tAreAssigned.permitID
            WHERE tAreAssigned.univID_phonenumber = ?
        """, (univID_phonenumber,))
        permit_info = curs.fetchall()

        if permit_info:
            print()
            for row in permit_info:
                permitID, permit_type, space_type, start_date, expiration_date, expiration_time = row
                # Printing all attributes of a permit
                print(f"Permit ID: {permitID}")
                print(f"Permit Type: {permit_type}")
                print(f"Space Type: {space_type}")
                print(f"Start Date: {start_date}")
                print(f"Expiration Date: {expiration_date}")
                print(f"Expiration Time: {expiration_time}")
                print(f"University ID/Phone Number: {univID_phonenumber}") # Reprinting the ID
                print()
        else:
            # Handling the case where a permit does not exist for this person
            print(f"No permit information found for university ID/phone number: {univID_phonenumber}")


    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print(f"Error getting permit information")
        print(f"SQLite error: {e}")
    
# Reporting the number of spaces that are available to park in given the type of spot a person is looking for along with the lot name
def availableSpaceNumberGivenType(lot_name: str, space_type: str):
        try:
            # Making sure the user provided us with a university ID or phone number
            if lot_name == "" or space_type == "":
                print("You must provide us with a lot name and space type that you wish to see available spaces for.")
                return
            # If the space has a availability status of 'available' we can return the number of spaces we get where the lot name and space type are also the same
            curs.execute("SELECT COUNT(*) FROM tSpaces WHERE lot_name = ? AND space_type = ? AND availability = 'Available'", (lot_name, space_type))
            available_space_count = curs.fetchone()[0]

            print(f"\nNumber of Available {space_type} Spaces in {lot_name}: {available_space_count}")

            # Select the first available space if it exists
            if (available_space_count > 0):
                curs.execute("SELECT space_number, zoneID, lot_name FROM tSpaces WHERE lot_name = ? AND space_type = ? AND availability='Available' LIMIT 1;", (lot_name, space_type))
                available_space_number, available_zoneID, available_lot_name = curs.fetchone()
                print(f"Space #{available_space_number} in {available_lot_name}, Zone {available_zoneID} is available.")
            else:
                print("No available spaces.")

        except sql.Error as e:
            print("Error counting available spaces by type")

# Counting the number of permits that have been requested but not approved or denyed
def count_pending_permits():
    try:
        curs.execute("SELECT COUNT(*) FROM tPermits WHERE expiration_date IS NULL AND expiration_time IS NULL;")
        number_pending = curs.fetchall()[0][0]

        print(f"\nNumber of pending permits: {number_pending}")

    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print(f"Error counting number of pending permits: {e}")