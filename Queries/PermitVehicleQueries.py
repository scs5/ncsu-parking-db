# This page is meant to handle any queries that involve maintaining permit or vehicle information.
# Tasks and Operations: Maintaining permits and vehicle information for each driver
import sqlite3 as sql
from load_tables import *
conn = sql.connect('parking.db')
curs = conn.cursor()
curs.execute("PRAGMA foreign_keys = ON;")

# (1)
# Approve permit
# univID_phonenumber, permitID, start and end dates are entered
# Happens after a permit has been requested
def approvePermits():
    permitID = input("Enter PermitID: ")
    if permitID == "":
        print("Permit ID is a required field for this operation.")
        return
    sqlQ = "SELECT * FROM tPermits WHERE permitID == "+permitID+";"
    curs.execute(sqlQ)
    result = curs.fetchall()
    print("RESULT:",result)
    if len(result) == 0: # Making sure the permit we are about to approve has been requested already
        print('No permit with this ID was found.')
        return
    if result[0][4] != None:
        print('The permit with this ID has already been approved.')
        return
    print(result)
    zoneID = input("Enter an existing zone ID: ")
    sql_status = "SELECT status from tDrivers WHERE univID_phonenumber IN (SELECT univID_phonenumber FROM tAreAssigned WHERE permitID =="+permitID+");"
    curs.execute(sql_status)
    status = curs.fetchall()[0][0]
    print("STATUS:",status)
    if status == "S" and len(zoneID)==1:
        print("Student drivers cannot park in this zone ("+zoneID+")")
        return
    if status == "V" and zoneID!="V":
        print("Visitor drivers cannot park in this zone ("+zoneID+")")
        return
    if status != "S" and len(zoneID)>1:
        print("Non-student drivers cannot park in this zone ("+zoneID+")")
        return
    # check if that space type exists in any of the lots with the given zone ID
    check_space = "SELECT * FROM tSpaces WHERE space_type =='"+result[0][2]+"' AND zoneID=='"+zoneID+"';"
    curs.execute(check_space)
    res = curs.fetchall()
    print(res)
    check_spaces = "SELECT * FROM tSpaces;"
    curs.execute(check_spaces)
    print(curs.fetchall())
    if len(res)==0:
        print('No spaces of type '+result[0][2]+" found in zone "+zoneID+" of any lots.")
        print('Would you like to proceed with approving the permit anyway? We recommend you try again with a zone ID containing this space type or deny this permit.')
        print("(1) Cancel approval.")
        print("(2) Proceed anyway.")
        choice1 = input()
        if choice1 != "2":
            return
    startDate = input("Enter the start date of the permit being approved (YYYY-MM-DD). If you wish to use the requested start date, click enter: ")
    if startDate == "":
        startDate =result[0][3]
        print(startDate)
    expirationDate = input("Enter the expiration date of the permit being approved (YYYY-MM-DD): ")
    expirationTime = input("Enter the expiration time of the permit being approved (XX:XX:XX): ")
    # if DATE(expirationDate)<DATE(startDate):
    #     print("Start date must fall before end date.")
    #     return
    # Making sure the user inputs all required fields to perform this functionality
    if permitID == "" or zoneID == "" or startDate == "" or expirationDate == "" or expirationTime == "":
        print("You must fill in all fields to perform this action.")
        return
    try:
        curs.execute("BEGIN TRANSACTION;")
        # Updating the following fields for the permit being approved
        # start date, expiration time, and expiration date
        # These fields not having a null value indicates that the permit was approved.
        print([startDate, expirationDate, expirationTime])

        update_query = "UPDATE tPermits SET start_date = ?, expiration_date = ?, expiration_time = ? WHERE permitID = ?"
        curs.execute(update_query, (startDate, expirationDate, expirationTime, permitID))
        # return

        # Adding the new permit information into tAllowsDriverToParkIn
        curs.execute("SELECT lot_name FROM tZones WHERE zoneID =='"+zoneID+"';")
        result = [l[0] for l in curs.fetchall()]
        print("LOTS:",result)
        if len(result) == 0:
            print('No zone with the given ZoneID was found.')
            raise Exception('Error: invalid data provided')
        for lotName in result:
            # Using our load function to add rows to the tAllowsDriverToParkIn table
            # load('tAllowsDriverToParkIn',[permitID, zoneID, lotName])
            insert_sql = "INSERT INTO tAllowsDriverToParkIn VALUES (?,?,?);"
            print(insert_sql)
            print([permitID, zoneID, lotName])
            curs.execute(insert_sql,[permitID,zoneID, lotName])
        curs.execute("COMMIT;")
        print("The permit has been approved.")
    except Exception as e:
    # Print the error message
        print(f"Exception: {e}")
        # If an error happens we print the message (useful for debugging the code)
        curs.execute("ROLLBACK;")
        print("There has been an error approving the permit.")

# (2)
# Deny Permits
# Happens after a permit has been requested but appoving that permit will violate some rules of our parking system
def denyPermit(permitID: str):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if permitID == "":
            print("You must enter the permit ID for the permit you wish to deny.")
            return

        # Making sure the permit we are about to update exists
        sqlQ = "SELECT * FROM tPermits WHERE permitID == "+permitID+";"
        curs.execute(sqlQ)
        result = curs.fetchall()
        if len(result) == 0: # Making sure the permit we are about to approve has been requested already
            print('No permit with this ID was found.')
            return
        if result[0][4] != None:
            print('The permit with this ID has already been approved.')
            return

        # Deleting the permit from the tPermits table because it break the parking system rules
        delete_query = "DELETE FROM tPermits WHERE permitID = ?"
        curs.execute(delete_query, (permitID))

        conn.commit()
        print("The permit has been denied.")
    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print("There has been an error denying the permit.")


# (3)
# Update Permits
def updatePermitInformation(permit_ID: int, permit_type: str, space_type: str, start_date: str, expiration_date: str, expiration_time: str):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if permit_ID == "":
            print("\nYou must enter the permit ID to perform this function.")
            return
        # Making sure the permit we are about to update exists
        sqlQ = "SELECT * FROM tPermits WHERE permitID == "+permit_ID+";"
        curs.execute(sqlQ)
        result = curs.fetchall()
        if len(result) == 0: # Making sure the permit we are about to approve has been requested already
            print('No permit with this ID was found.')
            return

        # Finding the permit that is associated with the provided permit ID
        curs.execute("SELECT * FROM tPermits WHERE permitID =="+permit_ID+";")
        existing_permit_info = curs.fetchone()

        # if existing_permit_info[0] == 0:
        #     print("This permit has not yet been requested")
        #     return

        # print(permit_type)
        # If the user simply clicks enter we keep the old value for that attribute
        # If the user enters something new, only then will the new attribute value be adapted
        if existing_permit_info:
            # Update permit information while retaining old values if input is empty
            permit_type = permit_type if permit_type != "" else existing_permit_info[1]
            space_type = space_type if space_type != "" else existing_permit_info[2]
            start_date = start_date if start_date != "" else existing_permit_info[3]
            expiration_date = expiration_date if expiration_date != "" else existing_permit_info[4]
            expiration_time = expiration_time if expiration_time != "" else existing_permit_info[5]

            # Update the permit with the new information
            curs.execute("UPDATE tPermits SET space_type=?, permit_type=?, start_date=?, expiration_date=?, expiration_time=? WHERE permitID = ?;",
                           (space_type, permit_type, start_date, expiration_date, expiration_time, permit_ID))

        conn.commit()
        print("Permit information updated successfully.")

    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print(f"Error updating the permit information: {e}")

# (4)
# Updating who the driver of a vehicle is
def updateDriverOfVehicle(old_univID_phonenumber: str, new_univID_phonenumber: str, license_number: str):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if old_univID_phonenumber == "" or new_univID_phonenumber == "" or license_number == "":
            print("You must fill in all fields.")
            return

        # Checking that a vehicle exists with the current owner
        # sqlQ = "SELECT * FROM tDrive WHERE license_number = ? AND univID_phonenumber = ?", (license_number, old_univID_phonenumber)
        curs.execute("SELECT * FROM tDrive WHERE license_number = ? AND univID_phonenumber = ?", (license_number, old_univID_phonenumber))
        result = curs.fetchall()
        if len(result) == 0: # Making sure the permit we are about to approve has been requested already
            print(f"No vehicle found with license number '{license_number}' and old owner '{old_univID_phonenumber}'.")
            return

        # Update the vehicle ownership information with the new owner (univID_phonenumber)
        update_query = "UPDATE tDrive SET univID_phonenumber = ? WHERE license_number = ?"
        curs.execute(update_query, (new_univID_phonenumber, license_number))

        # Commit the changes to the database
        conn.commit()
        print("Vehicle ownership information updated successfully.")
    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print(f"Error updating vehicle ownership information: {e}")


# (5)
# If a driver gets a new license plate, they are able to update their license number
def updateVehicleLicenseNumber(oldLicenseNumber: str, newLicenseNumber: str):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if oldLicenseNumber == "" or newLicenseNumber == "":
            print("You must fill in all fields.")
            return

        curs.execute("SELECT * FROM tVehicles WHERE license_number =='"+oldLicenseNumber+"';")
        result = curs.fetchall()
        if len(result) == 0: # Making sure the permit we are about to approve has been requested already
            print(f"The old license number does not exist.")
            return

        # Checks to see if a vehicle with the old license number exists in the system
        curs.execute("SELECT * FROM tVehicles WHERE license_number =='"+oldLicenseNumber+"';")
        vehicle_exists = curs.fetchone()[0]

        if vehicle_exists:
            # Update the license number of the vehicle
            curs.execute("UPDATE tVehicles SET license_number = ? WHERE license_number = ?", (newLicenseNumber, oldLicenseNumber))
            conn.commit()
            print(f"License number updated successfully. Old License Number: {oldLicenseNumber}, New License Number: {newLicenseNumber}")
        else:
            print(f"No vehicle found with the old license number: {oldLicenseNumber}")
    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print(f"Error updating vehicle license number: {e}")


# (6)
# Removing a vehicle if its not needed anymore
def removeVehicle(license_number: str):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if license_number == "":
            print("You must enter the license number for the vehicle you wish to remove from the system.")
            return

        # Checks to see if a vehicle with the license number exists in the system
        # sqlQ = "SELECT COUNT(*) FROM tVehicles WHERE license_number =='"+license_number+"';"
        curs.execute("SELECT * FROM tVehicles WHERE license_number =='"+license_number+"';")
        result = curs.fetchall()
        if len(result) == 0:
            print(f"No vehicle found with license number '{license_number}'")
            return

        # Deleting the vehicle associated with this license number from the database
        delete_query = "DELETE FROM tVehicles WHERE license_number =='"+license_number+"';"
        curs.execute(delete_query)

        conn.commit()
        print(f"Vehicle with license number '{license_number}' removed successfully.")

    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print("Error removing the vehicle.")


# (7)
# Adding a vehicle to the system under a driver (given their university ID or phone number)
def addVehicle(univID_phonenumber: str, license_number: str, model: str, color: str, manufacturer: str, year: int):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if univID_phonenumber == "" or license_number == "" or model == "" or color == "" or manufacturer == "" or year == "":
            print("You must fill in all fields.")
            return

        # Making sure the vehicle we are about to add to the database doesn't already exist
        # We want to avoid adding the same vehicle twice
        sql = "SELECT COUNT(*) FROM tVehicles WHERE license_number =='"+license_number+"';"
        # curs.execute("SELECT COUNT(*) FROM tVehicles WHERE license_number = ?;", (license_number))
        curs.execute(sql)

        result = curs.fetchone()

        # Printing a message for the user if the vehicle already exists and breaking out
        if result[0] > 0:
            print(f"A vehicle with license number '{license_number}' already exists in the database.")
            return

        # Making sure the driver of the vehicle is in the tDrivers table in our database
        sql = "SELECT COUNT(*) FROM tDrivers WHERE univID_phonenumber =='"+univID_phonenumber+"';"
        curs.execute(sql)
        result = curs.fetchone()
        # Printing a message to the user if the driver associated with the provided university ID/phone number does not exist
        if result[0] == 0:
            print(f"A driver with univID_phonenumber '{univID_phonenumber}' does not exists in the database.")
            return

        # This function is performed using a transaction
        curs.execute("BEGIN TRANSACTION;")
        try:
            # First we try inserting the vehicle into tVehicles
            insert_query = "INSERT INTO tVehicles (license_number, model, color, manufacturer, year) VALUES (?, ?, ?, ?, ?);"
            curs.execute(insert_query, (license_number, model, color, manufacturer, year))
        except sql.Error as e:
            # Printing a message for the user and performing a rollback if necessary
            print(f"Vehicle couldn't be added: {e}")
            curs.execute("ROLLBACK;")
            return

        # load('tVehicles',[license_number, model, color, manufacturer, year])
        try:
            # Inserting the relationship into the tDrive table
            insert_query = "INSERT INTO tDrive (license_number, univID_phonenumber) VALUES (?, ?);"
            curs.execute(insert_query, (license_number, univID_phonenumber))
        except sql.Error as e:
            # If the relationship cannot be added we also want to rollback the vehicle that got added one step above
            print(f"Vehicle and Person relationship couldn't be added: {e}")
            curs.execute("ROLLBACK;")
            return
        # load('tDrive',[license_number, univID_phonenumber])

        # Commit the changes to the database
        curs.execute("COMMIT;")
        print(f"Vehicle with license number '{license_number}' added successfully.")
    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print("Error adding the vehicle.")
        print(f"Error: {e}")


# (8)
# NOTE: You must first use addVehicle() then you may use this function
def addVehicleToPermit(univID: str, permitID: str):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if univID == "" or permitID == "":
            print("You must fill in all fields.")
            return

        # Check that this is indeed an employee that exists
        # sqlQ = "SELECT * FROM tDrivers WHERE univID_phonenumber =='"+univID+"' AND status == 'E';"
        curs.execute("SELECT * FROM tDrivers WHERE univID_phonenumber =='"+univID+"' AND status == 'E';")
        result = curs.fetchall()
        if len(result) == 0:
            print("This is not an employee university ID. You may not add another vehicle to your permit'")
            return

        # Check that this permitID exists
        sql = "SELECT COUNT(*) FROM tPermits WHERE permitID =='"+permitID+"';"
        curs.execute(sql)

        result = curs.fetchone()
        if result[0] == 0:
            print("This permit is not in the system. Vehicle cannot be added for this permit'")
            return

        # Ask for license number
        license_number = input("Enter the license number on the vehicle you wish to add for this permit: ")

        # Verify license number is present in tVehicles
        sql = "SELECT COUNT(*) FROM tVehicles WHERE license_number =='"+license_number+"';"
        curs.execute(sql)

        result = curs.fetchone()
        if result[0] == 0:
            print("This vehicle is not in the system. You must add the vehicle to the system before adding it to a permit'")
            return

        # Add row to tAreAssociatedWith with the license number and permit ID
        load('tAreAssociatedWith',[license_number, permitID])
        conn.commit()
        print("The vehicle has been added to the permit.")
    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print("There has been an error while adding the vehicle to the permit.")













# EXTRA
# Tyring to handle approving and denying in one method
# This will help with the following checks
# driver status 'S' & 'V'
#   --> 1 vehicle on permit
#   --> 1 permit
# 'E'
#   --> up to 2 vehicle on permit
#   --> 2 permit
# 'S' & 'E'
#   --> 1 additional permit
#       --> for ‘Special Events’ or ‘Park & Ride’
def approveDenyPermit(univID_phonenumber: str, permitID: str):
    try:
        # Making sure the user inputs all required fields to perform this functionality
        if permitID == "":
            print("You must provide the permit ID for the requested permit.")
            return

        # Obtaining...
        # type of permit
        # univID_phonenumber
        # status
        curs.execute("""
            SELECT tPermits.permit_type, tAreAssigned.univID_phonenumber, tDrivers.status
            FROM tPermits
            JOIN tAreAssigned ON tPermits.permitID = tAreAssigned.permitID
            JOIN tDrivers ON tAreAssigned.univID_phonenumber = tDrivers.univID_phonenumber
            WHERE tPermits.permitID = ?
        """, (permitID))

        result = curs.fetchone()

        if result:
            permit_type, univID_phonenumber, driver_status = result

            # Checking if the driver already has another permit
            curs.execute("""
                SELECT tPermits.permit_type, tPermits.permitID
                FROM tPermits
                JOIN tAreAssigned ON tPermits.permitID = tAreAssigned.permitID
                WHERE tAreAssigned.univID_phonenumber = ? AND tPermits.permit_type != ?
            """, (univID_phonenumber, permit_type))

            existing_permits = curs.fetchall()

            # Check how many permits the driver already has
            curs.execute("""
                SELECT COUNT(*) FROM tPermits
                JOIN tAreAssigned ON tPermits.permitID = tAreAssigned.permitID
                WHERE tAreAssigned.univID_phonenumber = ? AND tPermits.start_date = ?
            """, (univID_phonenumber, None))

            total_permits = curs.fetchone()[0]

            if existing_permits and total_permits >= 2:
                denyPermit(permitID)
                print("Permit denied. Driver already has two permits.")
                return
            elif permit_type in ('Residential', 'Commuter', 'Peak Hours') and total_permits >= 1 and driver_status != 'E':
                denyPermit(permitID)
                print("Permit denied. Maximum permits reached for this category.")
                return
            else:
                # Check rules and decide whether to approve or deny the permit
                if permit_type in ('Residential', 'Commuter', 'Peak Hours'):
                    if driver_status == 'S' and permit_type != 'Special Event' and permit_type != 'Park & Ride':
                        # Students can only have one permit, and it cannot be for special events or Park & Ride
                        denyPermit(permitID)
                        print("Permit denied. Students can only have one permit.")
                        return
                    elif driver_status == 'V' and permit_type != 'Special Event' and permit_type != 'Park & Ride':
                        # Visitors can only have one permit, and it cannot be for special events or Park & Ride
                        denyPermit(permitID)
                        print("Permit denied. Visitors can only have one permit.")
                        return
                    elif driver_status == 'E':
                        # Employees can have up to two permits
                        print("Permit approved. Employee permit.")
                    else:
                        # Other cases are not allowed
                        denyPermit(permitID)
                        print("Permit denied. Invalid permit type or status.")
                        return
                else:
                    # For other permit types, approve the permit
                    zoneID = input("Enter ZoneID: ")
                    startDate = input("Enter the start date of the permit being approved (XXXX-XX-XX): ")
                    expirationDate = input("Enter the expiration date of the permit being approved (XXXX-XX-XX): ")
                    expirationTime = input("Enter the expiration time of the permit being approved (XX:XX:XX): ")
                    approvePermits(permitID, zoneID, startDate, expirationDate, expirationTime)

        else:
            print(f"No permit found with permit ID: {permitID}")

    except sql.Error as e:
        # If an error happens we print the message (useful for debugging the code)
        print("There has been an error approving/denying the permit.")
