import sqlite3 as sql
import Queries.ReportQueries as execute
conn = sql.connect('parking.db')
curs = conn.cursor()


def generate_citation_report():
    """ Generate a report of all citations present in the system """
    execute.generateCompleteReport()


def generate_total_citations_report():
    """ Generate a report of all citations within a given time range. """
    startDate = input("Enter the start date of the time range for which you want to see citations (XXXX-XX-XX): ")
    endDate = input("Enter the end date of the time range for which you want to see citations (XXXX-XX-XX): ")
    execute.generateCitationsInRange(startDate, endDate)


def list_zones_for_lots():
    """ List all (zone, lot) pairs. """
    execute.listZonesForEachLot()


def cars_in_violation():
    """ Generate a report of all cars currently in violation (unpaid citations). """
    execute.carsCurrentlyInViolation()


def employees_with_permits():
    """ Report number of employees with permits. """
    zoneID = input("Which zone would you like to see the employees with permits: ")
    execute.employeesWithPermitInZone(zoneID)


def permit_info_by_id_or_phone():
    """ Report permit information for a specific driver. """
    univID_phonenumber = input("Enter your university ID (Students & Employees) OR phone number (Visitors): ")
    execute.permitInfoGivenIdNumber(univID_phonenumber)


def available_space_by_type():
    """ Report number of available spaces (and give a specific available space). """
    lot_name = input("What lot would you like to see available spaces for: ")
    space_type = input("Input the space type you are requesting to see available spaces for: ")
    execute.availableSpaceNumberGivenType(lot_name, space_type)


def count_pending_permits():
    """ Report number of pending permits. """
    execute.count_pending_permits()