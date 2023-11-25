import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()
curs.execute("PRAGMA foreign_keys = ON;")
import load_tables as insert

# Requesting Citation Appeal
def requestCitationAppeal(citationNumber: int):
    try:
        # Obtaining the current payment status of the citation with the provided citation number
        curs.execute("SELECT payment_status FROM tCitations WHERE citation_number = ?", (citationNumber))
        res = curs.fetchone()
        # Only if the the payment status is unpaid can we appeal it
        if res and res[0] == "Unpaid":
            curs.execute("UPDATE tCitations SET payment_status = 'Appealed' WHERE citation_number = ?;", (citationNumber))
            conn.commit()
            print("\nCitation appeal requested successfully.")
        else:
            print("\nCitation cannot be requested for appeal as the citation not existing or is already appealed or paid.")
    except sql.Error as e:
        print("Error requesting citation appeal")

# Deny Appeal (changes status to “appeal denied”)
def denyAppeal(citationNumber: int):
    try:
        # Obtaining the current payment status of the citation with the provided citation number
        curs.execute("SELECT payment_status FROM tCitations WHERE citation_number = ?", (citationNumber))
        res = curs.fetchone()
        # We check to make sure the appeal has been made (status = "Appealed")
        if res and res[0] == "Appealed":
            # We deny the appeal by changing the status back to unpaid for the citation
            curs.execute("UPDATE tCitations SET payment_status = 'Unpaid' WHERE citation_number = ?;", (citationNumber))
            conn.commit()
            print("\nCitation appeal denied successfully.")
        else:
            print("\nCitation appeal cannot be denied because citation not existing or is not in appealed status.")
    except sql.Error as e:
        print("Error denying citation appeal")

# Pay a Citation
def payCitation(citationNumber: int):
    try:
        # Obtaining the current payment status of the citation with the provided citation number
        curs.execute("SELECT payment_status FROM tCitations WHERE citation_number = ?", (citationNumber))
        res = curs.fetchone()
        # We check to make sure the citation being paid hasn;t already been made (status should still be unpaid)
        if res and res[0] == "Unpaid":
            # We set the status to paid to indicate that a payment has been made
            curs.execute("UPDATE tCitations SET payment_status = 'Paid' WHERE citation_number = ?;", (citationNumber))
            conn.commit()
            print("\nCitation paid successfully.")
        else:
            print("Citation cannot be paid due to citation not existing or being in unpaid status")
    except sql.Error as e:
        print("Error paying citation")

# Delete Citations for approving an appeal
def delete_citation(citation_number=None):

    try:
        # Obtaining the current payment status of the citation with the provided citation number
        curs.execute("SELECT payment_status FROM tCitations WHERE citation_number = ?", (citation_number))
        res = curs.fetchone()
        # If the citation has been appealed and the appeal has been approved, the citation can be deleted from tCitations
        if res and res[0] == "Appealed":
            curs.execute("DELETE FROM tCitations WHERE citation_number = ?;", (citation_number))
            conn.commit()
            print("\nCitation approved successfully.")
        else:
            print("Citation cannot be appealed due to citation not existing or being in appealed status")
    # Catching any errors that may occur
    except sql.Error as e:
        print("Error approving citation")

# Generating a citation for a vehicle that has made a violation
def generate_citation(licensePlate, citationDate, citationTime, parkinglotName, category):
    
    try:
        # Assigning a value to the fee based on the category of the violation - based on project narrative
        fee  = 0
        if category == "Invalid Permit":
            fee = 25
        elif category == "Expired Permit":
            fee = 30
        elif category == "No Permit":
            fee = 40
        else:
            # If the violation doesn't fall under one of these categories, it is invalid
            print("You have entered an invalid category. Please enter one of the following: No Permit, Expired Permit, Invalid Permit")
            return
        # We begin our transaction
        curs.execute("BEGIN TRANSACTION;")
        curs.execute("SELECT univID_phonenumber FROM tDrive WHERE tDrive.license_number = ?", (licensePlate,))
        # We obtain the driver of the vehicle getting the citation
        univID = curs.fetchone()
        curs.execute("SELECT tPermits.space_type FROM tPermits JOIN tAreAssigned ON tAreAssigned.permitID = tPermits.permitID WHERE tAreAssigned.univID_phonenumber = ?", univID)
        spaceTypes = curs.fetchall()
        # Handicap users will receive a 50% discount on all citation fees
        for spaceType in spaceTypes:
            if spaceType[0] == "Handicap":
                fee /= 2
                break
        # Adding a row to tCitations with a newly created citation with status unpaid
        tupl = (find_max(), category, citationDate, citationTime, str(fee), "Unpaid")
        curs.execute("INSERT INTO tCitations (citation_number, category, citation_date, citation_time, fee, payment_status) VALUES(?, ?, ?, ?, ?, ?);", tupl)
    except sql.Error as e:
        # Printing any errors that may occur
        print(f"Citation couldn't be added: {e}")
        return
    # Handling a rollback where the citation was unable to be added into the table
    curs.execute("SELECT citation_number FROM tCitations WHERE category  = ? AND citation_date = ? AND citation_time = ? AND fee = ?;", (category, citationDate, citationTime, fee))
    res = curs.fetchone()
    if not res and res[0]:
        print("Error in adding to tCitations when generating citation")
        curs.execute("ROLLBACK;")
        return
    # Creating the tuple to insert into tAreTicketedTo which is another table that will be impacted with the creation of a new citation
    tupl = (licensePlate, res[0])
    try:
        # Trying to insert
        curs.execute("INSERT INTO tAreTicketedTo (license_number, citation_number) VALUES(?, ?);", tupl)
    except sql.Error as e:
        # Error handling and rollback
        print(f"Citation couldn't be added: {e}")
        curs.execute("ROLLBACK;")
        return
    # Creating the tuple that will be inserted into tAreIssuedWithin
    tupl = (parkinglotName, res[0])
    try:
        curs.execute("INSERT INTO tAreIssuedWithin (lot_name, citation_number) VALUES(?, ?);", tupl)
    except sql.Error as e:
        # Error handling and rollback
        print(f"Citation couldn't be added: {e}")
        curs.execute("ROLLBACK;")
        return
    curs.execute("COMMIT;")
    print("Citation Successfully Generated")

# A function is used to detect if a vehicle has a violation in a given lot
# Change name?
def detect_citation(licensePlate, parkingLot):
    # We need to look at the tables: tAreAssociatedWith and tAllowsDriverToParkIn
    try:
        current_date = input("Input current date (YYYY-MM-DD): ")
        curs.execute("SELECT * FROM tAreAssociatedWith NATURAL JOIN tAllowsDriverToParkIn NATURAL JOIN tPermits WHERE lot_name = ? AND license_number = ? AND start_date < ? AND expiration_date > ?;", (parkingLot, licensePlate, current_date, current_date))
        res = curs.fetchall()
    except sql.Error as e:
        print(f"Error in detecting citation: {e}")
    # If we find that they can park in the lot they are not in violation
    if res:
        return False
    # If they cannot park their, they are in violation
    return True

# This helper function checks to see if the license plate is in the database
def detect_licenseplate(licensePlate):
    curs.execute("SELECT * FROM tVehicles WHERE license_number = ?", (licensePlate,))
    res = curs.fetchall()
    # return true if it is and false if the plate is not found
    if res and res[0]:
        return True
    return False

# Finding the biggest citation number in tCitations
# This helps us increment the citation number when we add a citation
def find_max():
    curs.execute("SELECT MAX(citation_number) FROM tCitations;")
    res = curs.fetchone()
    # If there are no citations in the system we set it as 1 initially
    if not res and not res[0]:
        return 1
    # Once citations are added we can increment each time
    else:
        return res[0] + 1

# Detects if the license plate exists and prints out all the citations for that license number
# Rename
def detect_license(license):
    # Making sure license number is entered
    if not license:
        print("License needs to be entered")
        return False
    # Checking for citations
    curs.execute("SELECT * FROM tCitations NATURAL JOIN tAreTicketedTo WHERE license_number = ?", (license,))
    res = curs.fetchall()
    if res and res[0]:
        for row in res:
            # Printing each citation
            print(row)
        return True
    else:
        return False

# Detects if a parking lot exists
def detect_parkinglot(parkinglot):
    # Making sure parking lot is entered
    if not parkinglot:
        print("Parking lot needs to be entered")
        return False
    # Checking for parking lot in tLots
    curs.execute("SELECT * FROM tLots WHERE lot_name = ?", (parkinglot,))
    res = curs.fetchall()
    # Return true if it exists and false otherwise
    if res and res[0]:
        return True
    return False
    