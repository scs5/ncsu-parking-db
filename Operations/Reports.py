# This file contains all the functions for Reports
# This file is solely for taking in user inputs
import sqlite3 as sql
import Queries.ReportQueries as execute
conn = sql.connect('parking.db')
curs = conn.cursor()

# Generating an overall report of all citations present in the system
def generate_citation_report():
    execute.generateCompleteReport()
    # print("You selected Generate a report for citations")

# Generating a report between a given time range (between 2 dates)
def generate_total_citations_report():
    startDate = input("Enter the start date of the time range for which you want to see citations (XXXX-XX-XX): ")
    endDate = input("Enter the end date of the time range for which you want to see citations (XXXX-XX-XX): ")
    execute.generateCitationsInRange(startDate, endDate)
    # print("You selected Generate a report for the total number of citations given in all zones in the lot for a given time range")

# Listing the (zone, lot) tuples
def list_zones_for_lots():
    execute.listZonesForEachLot()
    # print("You selected Return the list of zones for each lot as tuple pairs (lot, zone)")

# Checking what number of cars are currently in violation - payment status is either due or unpaid
def cars_in_violation():
    execute.carsCurrentlyInViolation()
    # print("You selected Return the number of cars that are currently in violation")

# Checking which employees have a valid permit for the zone that is inputted
def employees_with_permits():
    zoneID = input("Which zone would you like to see the employees with permits: ")
    execute.employeesWithPermitInZone(zoneID)
    # print("You selected Return the employees having permits for a given parking zone")

# Reports any permit information for a driver given either their university ID (S, E) or phone numeber (V)
def permit_info_by_id_or_phone():
    univID_phonenumber = input("Enter your university ID (Students & Employees) OR phone number (Visitors): ")
    execute.permitInfoGivenIdNumber(univID_phonenumber)
    # print("You selected Return permit information given an ID or phone number")

# Reports which space numbers are available in a parking lot given the type of space the user is looking for
def available_space_by_type():
    lot_name = input("What lot would you like to see available spaces for: ")
    space_type = input("Input the space type you are requesting to see available spaces for: ")
    execute.availableSpaceNumberGivenType(lot_name, space_type)
    # print("You selected Return available space numbers given a space type in a given parking lot")

# Counting the number of permits that have been requested but not approved or denyed
def count_pending_permits():
    execute.count_pending_permits()