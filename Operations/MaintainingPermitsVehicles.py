import sqlite3 as sql
import Queries.PermitVehicleQueries as execute
conn = sql.connect('parking.db')
curs = conn.cursor()
curs.execute("PRAGMA foreign_keys = ON;")


def assign_permits_to_drivers():
    """ Approve a permit """
    execute.approvePermits()


def deny_permit():
    """ Deny (delete) a permit. """
    permitID = input("Enter PermitID: ")
    execute.denyPermit(permitID)


def update_permit_info():
    """ Update a permit. """

    print("NOTE: For any fields you do not wish to modify, just press enter.")
    permit_ID = input("Enter the permit ID for the permit you wish to edit: ")
    permit_type = input("Enter the new permit type for this permit: ")
    space_type = input("Enter the new space type for this permit: ")
    start_date = input("Enter the new start date for this permit: ")
    expiration_date = input("Enter the new expiration date for this permit: ")
    expiration_time = input("Enter the new expiration time for this permit: ")
    execute.updatePermitInformation(permit_ID, permit_type, space_type, start_date, expiration_date, expiration_time)


def update_vehicle_ownership_info():
    """ Update vehicle ownership. """

    old_univID_phonenumber = input("Enter the old university ID (Students & Employees) OR phone number (Visitors) associated with the vehicle: ")
    new_univID_phonenumber = input("Enter the new university ID (Students & Employees) OR phone number (Visitors) associated with the vehicle: ")
    license_number = input("Enter the license number on the vehicle: ")
    execute.updateDriverOfVehicle(old_univID_phonenumber, new_univID_phonenumber, license_number)


def update_vehicle_license_plate():
    """ Update vehicle's license plate. """

    old_license_number = input("Enter the old license number on the vehicle: ")
    new_license_number = input("Enter the new license number on the vehicle: ")
    execute.updateVehicleLicenseNumber(old_license_number, new_license_number)


def remove_vehicle():
    """ Delete vehicle from database. """
    license_number = input("Enter the license number on the vehicle: ")
    execute.removeVehicle(license_number)


def add_vehicles():
    """ Add vehicle to database. """

    univID_phonenumber = input("Enter your university ID (Students & Employees) OR phone number (Visitors): ")
    license_number = input("Enter the license number on the vehicle: ")
    model = input("Enter the model of the vehicle: ")
    color = input("Enter the color of the vehicle: ")
    manufacturer = input("Enter the manufacturer of the vehicle: ")
    year = input("Enter the year of the vehicle: ")
    execute.addVehicle(univID_phonenumber, license_number, model, color, manufacturer, year)


def add_vehicle_to_permit():
    """ Add vehicle to a permit. """

    employee = input("Are you an employee? (Yes/No): ")
    if employee == "No" or employee == "no":
        print("You must be an employee to request another vehicle on your permit.")
        return
    else:
        univID_phonenumber = input("Enter your university ID: ")
        permit_ID = input("Enter the permit ID for the permit you wish to add a vehicle onto: ")
        execute.addVehicleToPermit(univID_phonenumber, permit_ID)