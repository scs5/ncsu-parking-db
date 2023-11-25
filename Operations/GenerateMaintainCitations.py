# This file contains functions for Generating and maintaining citations
import Queries.CitationQueries as execute
import datetime
import re


# This method completes the following functionality:
# Before generating a citation, detect parking violations by checking if a car has a valid permit in the lot. 
def detect_parking_violations():
    # First we take in any inputs that we need to complete the action
    licensePlate = input("Input the car's license plate: ")
    parkingLot = input("Input the parking lot: ")
    # If either field is empty, we return out of the method
    if not licensePlate or not parkingLot:
        print("fields must be filled")
        return
    # We then check to make sure the license plate that was provided exists
    if not execute.detect_licenseplate(licensePlate):
        print("license plate doesn't exist")
        return
    # We then check to make sure the parking lot that was provided exists
    if not execute.detect_parkinglot(parkingLot):
        print("parking lot doesn't exist")
        return
    # We are able to execute the query if we have all the proper information provided
    res = execute.detect_citation(licensePlate, parkingLot)
    if res:
        print("The license plate, " + licensePlate + ", is in violation in parking lot, " + parkingLot)
    else:
        print("no violation detected")

# Generate appropriate information for all the citations that a driver has
def print_citation_numbers(univID):
    # For this function we need the university ID/phone number to be able to search up the citations under the driver
    citation_numbers = execute.detect_univ(univID)
    # Here we print the information out
    output = "Your citation numbers: "
    for cnum in citation_numbers:
        output += str(cnum[0]) + ", "
    print(output)

# Generating all the citations under a vehicle
def generate_citation():
    # For this method we need the license plate number to search the vehicle
    licensePlate = input("Please provide an existing license plate: ")
    # Handling the case where the license plate is not inputted - user clicks enter
    if not licensePlate:
         print("No License Plate inputted.")
         return
    # Handling the case where the license plate does not exist
    if not execute.detect_licenseplate(licensePlate):
        print("License Plate does not exist.")
        return
    # if doesn't exist, then it will print error message
    # Asking for citation date
    citationDate = input("Please provide a date in the following format (YYYY-MM-DD): ")
    # Handling the case where the citation date is invalidly entered
    if not is_valid_date(citationDate):
        print("You inputted an invalid date.")
        return
    # Asking for citation time
    citationTime = input("Please provide a time in the following format (HH:MM:SS): ")
    # Handling the case where the citation time is invalidly entered
    if not is_valid_time(citationTime):
        print("You inputted an invalid time.")
        return
    # Asking for parking lot name
    parkinglotName = input("Input the parking lot name of the citation: ")
    # Handling the case where the parking lot doesn't exist in the system
    if not execute.detect_parkinglot(parkinglotName):
        print("Parking lot doesn't exist.")
        return
    # Asking for citation category
    category = input("Input the category of the citation: ")
    # We may now proceed to trying to execute the query with all the inputs
    execute.generate_citation(licensePlate,citationDate,citationTime, parkinglotName, category)


# Approving a citation appeal
def approve_appeal():
    # Asking for license number that the citation is under
    license = input("Please enter a valid license number: ")
    # Handling the case where the license number doesn't exist in the system - it's invalid
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    # Asking for citation number
    citationNumber = input("Input the citation number you would like to appeal: ")
    #logic to check citation number has appeal in the status column
    print("You selected Maintain appropriate information for each citation")
    execute.delete_citation(citationNumber)

# Paying the fee of a citation
def pay_citation():
    # Asking for license number that the citation is under
    license = input("Please enter a valid license number: ")
    # Handling the case where the license number doesn't exist in the system - it's invalid
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    # Asking for citation number
    citationNumber = input("Input the citation number you would like to pay: ")
    execute.payCitation(citationNumber)

# Appeal a citation
def appeal_citation():
    # Asking for license number that the citation is under
    license = input("Please enter a valid license number: ")
    # Handling the case where the license number doesn't exist in the system - it's invalid
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    # Asking for citation number
    citationNumber = input("Input the citation number you would like to request appeal for: ")
    execute.requestCitationAppeal(citationNumber)

# Rejecting a citation appeal
def reject_appeal():
    # Asking for license number that the citation is under
    license = input("Please enter a valid license number: ")
    # Handling the case where the license number doesn't exist in the system - it's invalid
    if not execute.detect_license(license):
        print("Invalid license.")
        return
    # Asking for citation number
    citationNumber = input("Input the citation number you would like to reject appeal for: ")
    execute.denyAppeal(citationNumber)

# Function that helps us detect whether a date that a user inputs is valid
def is_valid_date(date_string):
    # Regular expression pattern for "YYYY-MM-DD" format
    if not date_string:
        return False
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    # Check if the date_string matches the pattern
    if not re.match(pattern, date_string):
        return False
    
    # Parse the date using datetime.strptime and check if it's a valid calendar date
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
# Function that helps us detect whether a time that a user inputs is valid
def is_valid_time(time_string):
    # Regular expression pattern for "HH:MM:SS" format
    if not time_string:
        return False
    pattern = r'^\d{2}:\d{2}:\d{2}$'
    
    # Check if the time_string matches the pattern
    if not re.match(pattern, time_string):
        return False
    
    # Parse the time using datetime.strptime and check if it's a valid time
    try:
        datetime.datetime.strptime(time_string, "%H:%M:%S")
        return True
    except ValueError:
        return False
