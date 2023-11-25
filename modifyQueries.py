import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()

curs.execute("PRAGMA foreign_keys = 1")

# Update Driver Information
def updateDriverInfo(univID_phonenumber: str, newName: str, newStatus: str):
    try:
        update_query = "UPDATE tDrivers SET name = ?, status = ? WHERE univID_phonenumber = ?;"
        curs.execute(update_query, (newName, newStatus, univID_phonenumber))
        conn.commit()
        print("Driver information updated successfully.")
    except sql.Error as e:
        # print(curs.fetchall)
        # print(sql.Error.args)
        print("Error updating driver information.")


# Update Parking Lot Information
def updateParkingLotInfo(oldLotName: str, newLotName: str, newAddress: str):
    print('input',oldLotName,newLotName,newAddress)
    try:
        # Check if the old lot exists
        curs.execute("SELECT COUNT(*) FROM tLots WHERE lot_name = ?;", (oldLotName,))
        result = curs.fetchone()

        # Making sure that the lot exists
        if result[0] == 0:
            print("The lot you are trying to modify does not exist")
            return

        # Making sure the new lot name & new address aren't already in use
        curs.execute("SELECT COUNT(*) FROM tLots WHERE lot_name = ? AND address = ?;", (newLotName, newAddress))
        result = curs.fetchone()

        if result[0] > 0:
            print("A parking lot with this name and address already exists")
            return
        update_query = "UPDATE tLots SET lot_name = ?, address = ? WHERE lot_name = ?;"
        curs.execute(update_query, (newLotName, newAddress, oldLotName))

        conn.commit()
        print("The parking lot information has been updated successfully.")
    except sql.Error as e:
        print("Error updating parking lot information.")


# Update Space Information
def updateSpace(space_number: int, lotName: str, zoneID: str,  newAvailability: str, newSpaceType: str):
    try:
        # Checking if that space exists
        curs.execute("SELECT COUNT(*) FROM tSpaces WHERE space_number = ? AND lot_name = ? AND zoneID = ?", (space_number, lotName, zoneID))
        result = curs.fetchone()

        # Making sure the space we want to update exists
        if result[0] == 0:
            print("This space doesn't exist.")
            return

        update_query = "UPDATE tSpaces SET availability = ?, space_type = ? WHERE space_number = ? AND lot_name = ? AND zoneID = ?"
        curs.execute(update_query, (newAvailability, newSpaceType, space_number, lotName, zoneID))

        conn.commit()
        print("The space information has been updated successfully.")
    except sql.Error as e:
        print("Error updating space information.")


# Update Vehicle
# Q. Why are we just updating the color of a vehicle?
def updateVehicle(licenseNumber: str, newColor: str):
    try:
        curs.execute("SELECT COUNT(*) FROM tVehicles WHERE license_number = ?", (licenseNumber))
        result = curs.fetchone()

        if result[0] == 0:
            print("A vehicle with this license number does not exist.")
            return

        update_query = "UPDATE tVehicles SET color = ? WHERE license_number = ?"
        curs.execute(update_query, (newColor, licenseNumber))

        conn.commit()
        print("The vehicles information has been updated successfully.")
    except sql.Error as e:
        print("Error updating the vehicles information.")


# Approve permit (start and end dates are entered)
# More checks may need to be added to this one
def approvePermits(permitID: int, startDate: str, expirationDate: str, expirationTime: str):
    try:
        curs.execute("SELECT COUNT(*) FROM tPermits WHERE permitID = ?", (permitID))
        result = curs.fetchone()

        if result[0] == 0:
            print("There is no permit found with this ID")
            return

        update_query = "UPDATE tPermits SET start_date = ?, expiration_date = ?, expiration_time = ? WHERE permitID = ?"
        curs.execute(update_query, (startDate, expirationDate, expirationTime, permitID))

        conn.commit()
        print("The permit has been approved.")
    except sql.Error as e:
        print("There has been an error approving the permit.")


# Update a Zone
def updateZone(lotName: str, oldZoneID: str, newZoneID: str):
    try:
        curs.execute("SELECT COUNT(*) FROM tZones WHERE lot_name = ? AND zoneID = ?;", [lotName, oldZoneID])
        result = curs.fetchone()
        print('result',result)
        if result[0] == 0:
            print("There is not a zone with this ID in this lot.")
            return

        update_query = "UPDATE tZones SET zoneID = ? WHERE lot_name = ? AND zoneID = ?;"
        curs.execute(update_query, [newZoneID, lotName, oldZoneID])

        conn.commit()
        print("The zone infomration has been updated successfully")
    except Exception as e:
        print(e)
        print("There has been an error updating the zone information.")


# Requesting Citation Appeal
def requestCitationAppeal(citationNumber: int):
    try:
        curs.execute("SELECT COUNT(*) FROM tCitations WHERE citation_number = ?", (citationNumber))
        result = curs.fetchone()

        if result[0] == 0:
            print("No citation found with this citation number")
            return

        update_query = "UPDATE tCitations SET payment_status = 'appealed' WHERE citation_number = ?"
        curs.execute(update_query, (citationNumber))

        conn.commit()
        print("Citation appeal requested successfully.")
    except sql.Error as e:
        print("Error requesting citation appeal")


# Deny Appeal (changes status to “appeal denied”)
def denyAppeal(citationNumber: int):
    try:
        curs.execute("SELECT COUNT(*) FROM tCitations WHERE citation_number = ?", (citationNumber))
        result = curs.fetchone()

        if result[0] == 0:
            print("No citation with this citation number found.")
            return
        update_query = "UPDATE tCitations SET payment_status = 'appeal denied' WHERE citation_number = ?"
        curs.execute(update_query, (citationNumber))

        conn.commit()
        print("Citation appeal has been denyed successfully.")
    except sql.Error as e:
        print("Error denying citation appeal.")


# Pay a Citation
def payCitation(citationNumber: int):
    try:
        curs.execute("SELECT COUNT(*) FROM tCitations WHERE citation_number = ? AND payment_status IN ('unpaid', 'appeal denied')", (citationNumber))
        result = curs.fetchone()

        if result[0] == 0:
            print("No citation with this citation number found.")
            return

        update_query = "UPDATE tCitations SET payment_status = 'paid' WHERE citation_number = ?"
        curs.execute(update_query, (citationNumber))

        conn.commit()
        print("Citation paid successfully")
    except sql.Error as e:
        print("Error paying the citation")


# Update Permits
def updatePermitInformation(permitID: int, newPermitType: str, newSpaceType: str):
    try:
        curs.execute("SELECT COUNT(*) FROM tPermits WHERE permitID = ?", (permitID))
        result = curs.fetchone()

        if result[0] == 0:
            print("No permit found with this permitID")
            return

        update_query = "UPDATE tPermits SET permit_type = ?, space_type = ? WHERE permitID = ?"
        curs.execute(update_query, (newPermitType, newSpaceType, permitID))

        conn.commit()
        print("Permit information updated successfully.")

    except sql.Error as e:
        print("Error updating the permit information.")
# conn.close()
