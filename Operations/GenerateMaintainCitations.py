import Queries.CitationQueries as execute
from utils import *


def detect_parking_violations():
    """ Before generating a citation, detect parking violations by checking 
        if a car has a valid permit in the lot.  """
    
    # User enters license plate and parking lot
    licensePlate = input("Input the car's license plate: ")
    parkingLot = input("Input the parking lot: ")

    # Error checking
    if not licensePlate or not parkingLot:
        print("Fields must be filled.")
        return
    if not execute.detect_licenseplate(licensePlate):
        print("License plate doesn't exist.")
        return
    if not execute.detect_parkinglot(parkingLot):
        print("Parking lot doesn't exist.")
        return
    
    # Execute SQL
    res = execute.detect_citation(licensePlate, parkingLot)
    if res:
        print("The license plate, " + licensePlate + ", is in violation in parking lot, " + parkingLot)
    else:
        print("no violation detected")


def print_citation_numbers(univID):
    """ Print all citation numbers associated with a driver. """

    citation_numbers = execute.detect_univ(univID)
    output = "Your citation numbers: "
    for cnum in citation_numbers:
        output += str(cnum[0]) + ", "
    print(output)


def generate_citation():
    """ Generate a citation. """

    # User enters license plate
    licensePlate = input("Please provide an existing license plate: ")
    # Error handling
    if not licensePlate:
         print("No License Plate inputted.")
         return
    if not execute.detect_licenseplate(licensePlate):
        print("License Plate does not exist.")
        return
    
    # User enters date
    citationDate = input("Please provide a date in the following format (YYYY-MM-DD): ")
    # Error handling
    if not is_valid_date(citationDate):
        print("You inputted an invalid date.")
        return
    
    # User enters time
    citationTime = input("Please provide a time in the following format (HH:MM:SS): ")
    # Error handling
    if not is_valid_time(citationTime):
        print("You inputted an invalid time.")
        return
    
    # User enters parking lot name
    parkinglotName = input("Input the parking lot name of the citation: ")
    # Error handling
    if not execute.detect_parkinglot(parkinglotName):
        print("Parking lot doesn't exist.")
        return
    
    # User enters citatation category
    category = input("Input the category of the citation: ")

    # Execute SQL
    execute.generate_citation(licensePlate,citationDate,citationTime, parkinglotName, category)


def approve_appeal():
    """ Approve a citation appeal. """

    # User enters licence plate number
    license = input("Please enter a valid license number: ")
    # Error handling
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    
    # User enters citation number
    citationNumber = input("Input the citation number you would like to appeal: ")

    # Execute SQL
    execute.delete_citation(citationNumber)


def pay_citation():
    """ Pay the fee of a citation. """

    # User enters license plate number
    license = input("Please enter a valid license number: ")
    # Error handling
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    
    # Enter citation number
    citationNumber = input("Input the citation number you would like to pay: ")

    # Execute SQL
    execute.payCitation(citationNumber)


def appeal_citation():
    """ Appeal a citation. """

    # User enters license plate number
    license = input("Please enter a valid license number: ")
    # Error handling
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    
    # User enters citation number
    citationNumber = input("Input the citation number you would like to request appeal for: ")

    # Execute SQL
    execute.requestCitationAppeal(citationNumber)


def reject_appeal():
    """ Deny a citation appeal. """

    # User enters license plate number
    license = input("Please enter a valid license number: ")
    # Error handling
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    
    # User enters citation number
    citationNumber = input("Input the citation number you would like to reject appeal for: ")

    # Execute SQL
    execute.denyAppeal(citationNumber)