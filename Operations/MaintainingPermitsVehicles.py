# This file contains functions for Maintaining permits and vehicle information
# This file is solely for taking in user inputs
import sqlite3 as sql
import Queries.PermitVehicleQueries as execute
conn = sql.connect('parking.db')
curs = conn.cursor()

# (1)
# Approve permit
# - assigns a zone
def assign_permits_to_drivers():
    # permitID = input("Enter PermitID: ")
    # zoneID = input("Enter ZoneID: ")
    # startDate = input("Enter the start date of the permit being approved (XXXX-XX-XX): ")
    # expirationDate = input("Enter the expiration date of the permit being approved (XXXX-XX-XX): ")
    # expirationTime = input("Enter the expiration time of the permit being approved (XX:XX:XX): ")
    # execute.approvePermits(permitID, zoneID, startDate, expirationDate, expirationTime)
    execute.approvePermits()
    # print("You selected Assign permits to drivers according to their status")


# (2)
# Deny a permit request
def deny_permit():
    permitID = input("Enter PermitID: ")
    execute.denyPermit(permitID)


# (3)
# Edit a permit
def update_permit_info():
    # Edit a permit
    print("NOTE: For any fields you do not wish to modify, just press enter.")
    permit_ID = input("Enter the permit ID for the permit you wish to edit: ")
    permit_type = input("Enter the new permit type for this permit: ")
    space_type = input("Enter the new space type for this permit: ")
    start_date = input("Enter the new start date for this permit: ")
    expiration_date = input("Enter the new expiration date for this permit: ")
    expiration_time = input("Enter the new expiration time for this permit: ")
    execute.updatePermitInformation(permit_ID, permit_type, space_type, start_date, expiration_date, expiration_time)
    # print("You selected Update permit information")

# (4)
# Update vehicle driver
def update_vehicle_ownership_info():
    # Update vehicle driver?
    # Need old univID_phonenumber, new univID_phonenumber and vehicle license number
    old_univID_phonenumber = input("Enter the old university ID (Students & Employees) OR phone number (Visitors) associated with the vehicle: ")
    new_univID_phonenumber = input("Enter the new university ID (Students & Employees) OR phone number (Visitors) associated with the vehicle: ")
    license_number = input("Enter the license number on the vehicle: ")
    execute.updateDriverOfVehicle(old_univID_phonenumber, new_univID_phonenumber, license_number)
    # print("You selected Update vehicle ownership information")

# (5)
# Edit vehicle info: license plate
def update_vehicle_license_plate():
    # Parameters = license_number: str
    old_license_number = input("Enter the old license number on the vehicle: ")
    new_license_number = input("Enter the new license number on the vehicle: ")
    execute.updateVehicleLicenseNumber(old_license_number, new_license_number)
    # print("You selected Enter vehicle information")

# (6)
def remove_vehicle():
    license_number = input("Enter the license number on the vehicle: ")
    execute.removeVehicle(license_number)
    #print("You selected Remove vehicle")

# (7)
def add_vehicles():
    # Same as enter_vehicle_ownership_info ???
    univID_phonenumber = input("Enter your university ID (Students & Employees) OR phone number (Visitors): ")
    license_number = input("Enter the license number on the vehicle: ")
    model = input("Enter the model of the vehicle: ")
    color = input("Enter the color of the vehicle: ")
    manufacturer = input("Enter the manufacturer of the vehicle: ")
    year = input("Enter the year of the vehicle: ")
    execute.addVehicle(univID_phonenumber, license_number, model, color, manufacturer, year)
    # print("You selected Add vehicles")


# # (8)
def add_vehicle_to_permit():
    employee = input("Are you an employee? (Yes/No): ")
    if employee == "No" or employee == "no":
        print("You must be an employee to request another vehicle on your permit.")
        return
    else:
        univID_phonenumber = input("Enter your university ID: ")
        permit_ID = input("Enter the permit ID for the permit you wish to add a vehicle onto: ")
        execute.addVehicleToPermit(univID_phonenumber, permit_ID)
