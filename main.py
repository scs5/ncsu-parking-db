import Operations.InformationProcessing as InformationProcessing
import Operations.MaintainingPermitsVehicles as MaintainingPermitsVehicles
import Operations.GenerateMaintainCitations as GenerateMaintainCitations
import Operations.Reports as Reports
from Queries.CitationQueries import *
from utils import *


# Information processing: 
# Enter/update/delete basic information about drivers parking lots, zones, spaces, and permits. 
# Assign zones to each parking lot and a type to a given space. 
def information_processing(option: int):
    if option == 1:
        InformationProcessing.enter_info_about_drivers()
    elif option == 2:
        InformationProcessing.enter_info_about_parking_lots()
    elif option == 3:
        InformationProcessing.enter_info_about_zone()
    elif option == 4:
        InformationProcessing.enter_info_about_spaces()
    elif option == 5:
        InformationProcessing.enter_info_about_permits()
    elif option == 6:
        InformationProcessing.update_info_about_drivers()
    elif option == 7:
        InformationProcessing.update_info_about_parking_lots()
    elif option == 8:
        InformationProcessing.update_info_about_zone()
    elif option == 9:
        InformationProcessing.update_info_about_spaces()
    elif option == 10:
        InformationProcessing.delete_info_about_drivers()
    elif option == 11:
        InformationProcessing.delete_info_about_parking_lots()
    elif option == 12:
        InformationProcessing.delete_info_about_zone()
    elif option == 13:
        InformationProcessing.delete_info_about_spaces()
    elif option == 14:
        InformationProcessing.delete_info_about_permits()


# Maintaining permits and vehicle information for each driver: 
# Assign permits to drivers according to their status. 
# Enter/update permit information and vehicle ownership information, including remove or add vehicles.
def maintain_permits_and_vehicle_info(option: int):
    # print("You selected Maintaining permits and vehicle information for each driver")
    if option == 1:
        MaintainingPermitsVehicles.assign_permits_to_drivers()
    elif option == 2:
        MaintainingPermitsVehicles.deny_permit()
    elif option == 3:
        MaintainingPermitsVehicles.update_permit_info()
    elif option == 4:
        MaintainingPermitsVehicles.update_vehicle_ownership_info()
    elif option == 5:
        MaintainingPermitsVehicles.update_vehicle_license_plate()
    elif option == 6:
        MaintainingPermitsVehicles.remove_vehicle()
    elif option == 7:
        MaintainingPermitsVehicles.add_vehicles()
    elif option == 8:
        MaintainingPermitsVehicles.add_vehicle_to_permit()


# Generating and maintaining citations: 
# Generate/maintain appropriate information for each citation. Before generating a citation, detect parking violations by checking if a car has a valid permit in the lot. 
# Drivers have the ability to pay or appeal citations.
def generate_and_maintain_citations(option: int):
    # print("You selected Generating and maintaining citations")
    if option == 1:
        GenerateMaintainCitations.detect_parking_violations()
    elif option == 2:
        GenerateMaintainCitations.generate_citation()
    elif option == 3:
        GenerateMaintainCitations.approve_appeal()
    elif option == 4:
        GenerateMaintainCitations.pay_citation()
    elif option == 5:
        GenerateMaintainCitations.reject_appeal()
    elif option == 6:
        GenerateMaintainCitations.appeal_citation()


# Reports: Generate a report for citations. For each lot, generate a report for the total number of citations given in all zones in the lot for a given time range (e.g., monthly or annually). 
# Return the list of zones for each lot as tuple pairs (lot, zone). 
# Return the number of cars that are currently in violation. 
# Return the number of employees having permits for a given parking zone. 
# Return permit information given an ID or phone number. 
# Return an available space number given a space type in a given parking lot.
def generate_reports(option: int):
    # print("You selected Reports")
    if option == 1:
        Reports.generate_citation_report()
    elif option == 2:
        Reports.generate_total_citations_report()
    elif option == 3:
        Reports.list_zones_for_lots()
    elif option == 4:
        Reports.cars_in_violation()
    elif option == 5:
        Reports.employees_with_permits()
    elif option == 6:
        Reports.permit_info_by_id_or_phone()
    elif option == 7:
        Reports.available_space_by_type()
    elif option == 8:
        Reports.count_pending_permits()


def menu():
    # Main menu
    while True:
        print("\nMain Menu:")
        print("(0) Load Demo Data")
        print("(1) Information Processing")
        print("(2) Maintaining Permit and Vehicle Information")
        print("(3) Generating and Maintaining Citations")
        print("(4) Reports")
        print("(5) Quit")

        choice = input("Select an option: ")

        if choice == '0':
            load_demo_data()
        elif choice == '1':
            while True:
                print("\nInformation Processing:")
                print("(1) Enter information about drivers") # Need univID_phonenumber
                print("(2) Enter information about parking lots")
                print("(3) Enter information about zone")
                print("(4) Enter information about spaces")
                print("(5) Enter information about permits")
                print("(6) Update information about drivers") # Need univID_phonenumber #checked
                print("(7) Update information about parking lots")
                print("(8) Update information about zone")
                print("(9) Update information about spaces")
                print("(10) Delete information about drivers") # Need univID_phonenumber #checked
                print("(11) Delete information about parking lots")
                print("(12) Delete information about zone")
                print("(13) Delete information about spaces")
                print("(14) Delete information about permits")
                print("(15) Back to Main Menu")

                info_processing_choice = input("Select an option (1-15): ")

                if info_processing_choice == '1':
                    information_processing(1)
                elif info_processing_choice == '2':
                    information_processing(2)
                elif info_processing_choice == '3':
                    information_processing(3)
                elif info_processing_choice == '4':
                    information_processing(4)
                elif info_processing_choice == '5':
                    information_processing(5)
                elif info_processing_choice == '6':
                    information_processing(6)
                elif info_processing_choice == '7':
                    information_processing(7)
                elif info_processing_choice == '8':
                    information_processing(8)
                elif info_processing_choice == '9':
                    information_processing(9)
                elif info_processing_choice == '10':
                    information_processing(10)
                elif info_processing_choice == '11':
                    information_processing(11)
                elif info_processing_choice == '12':
                    information_processing(12)
                elif info_processing_choice == '13':
                    information_processing(13)
                elif info_processing_choice == '14':
                    information_processing(14)
                elif info_processing_choice == '15':
                    break
                # elif info_processing_choice == '16':
                #     break
                else:
                    print("Invalid option. Please select a valid option (1-20).")
        elif choice == '2':
            while True:
                print("\nMaintaining permits and vehicle information:")
                print("(1) Approve a permit request") # Need univID_phonenumber
                print("(2) Deny a permit request") # Need univID_phonenumber
                print("(3) Update permit information") # Need univID_phonenumber
                print("(4) Update vehicle driver") # Need univID_phonenumber
                print("(5) Update vehicle license plate") # Need univID_phonenumber
                print("(6) Remove vehicle") # Need univID_phonenumber
                print("(7) Add vehicles") # Need univID_phonenumber
                print("(8) Add vehicle to a permit")
                print("(9) Back to Main Menu")

                permits_and_vehicles_choice = input("Select an option (1-9): ")

                if permits_and_vehicles_choice == '1':
                    maintain_permits_and_vehicle_info(1)
                elif permits_and_vehicles_choice == '2':
                    maintain_permits_and_vehicle_info(2)
                elif permits_and_vehicles_choice == '3':
                    maintain_permits_and_vehicle_info(3)
                elif permits_and_vehicles_choice == '4':
                    maintain_permits_and_vehicle_info(4)
                elif permits_and_vehicles_choice == '5':
                    maintain_permits_and_vehicle_info(5)
                elif permits_and_vehicles_choice == '6':
                    maintain_permits_and_vehicle_info(6)
                elif permits_and_vehicles_choice == '7':
                    maintain_permits_and_vehicle_info(7)
                elif permits_and_vehicles_choice == '8':
                    maintain_permits_and_vehicle_info(8)
                elif permits_and_vehicles_choice == '9':
                    break
                else:
                    print("Invalid option. Please select a valid option (1-9).")
        elif choice == '3':
            while True:
                print("\nGenerating and maintaining citations:")
                print("(1) Detect parking violations by checking if a car has a valid permit in the lot") # Need univID_phonenumber
                print("(2) Generate citation") # Need univID_phonenumber
                print("(3) Approve a citation appeal")
                print("(4) Pay citation")
                print("(5) Deny citation appeal")
                print("(6) Request an appeal of citation")
                print("(7) Back to Main Menu")

                citations_choice = input("Select an option (1-6): ")

                if citations_choice == '1':
                    generate_and_maintain_citations(1)
                elif citations_choice == '2':
                    generate_and_maintain_citations(2)
                elif citations_choice == '3':
                    generate_and_maintain_citations(3)
                elif citations_choice == '4':
                    generate_and_maintain_citations(4)
                elif citations_choice == '5':
                    generate_and_maintain_citations(5)
                elif citations_choice == '6':
                    generate_and_maintain_citations(6)
                elif citations_choice == '7':
                    break
                else:
                    print("Invalid option. Please select a valid option (1-6).")
        elif choice == '4':
            while True:
                print("\nReports:")
                print("(1) Generate a report for citations")
                print("(2) Generate a report for the total number of citations issued within a lot for a given time range")
                print("(3) Return the list of zones for each lot as tuple pairs (lot, zone)")
                print("(4) Return the number of cars that are currently in violation")
                print("(5) Return the number of employees having permits for a given parking zone")
                print("(6) Return permit information given an ID or phone number") # Need univID_phonenumber
                print("(7) Return an available space number given a space type in a given parking lot")
                print("(8) Return number of pending permits")
                print("(9) Back to Main Menu")

                reports_choice = input("Select an option (1-8): ")

                if reports_choice == '1':
                    generate_reports(1)
                elif reports_choice == '2':
                    generate_reports(2)
                elif reports_choice == '3':
                    generate_reports(3)
                elif reports_choice == '4':
                    generate_reports(4)
                elif reports_choice == '5':
                    generate_reports(5)
                elif reports_choice == '6':
                    generate_reports(6)
                elif reports_choice == '7':
                    generate_reports(7)
                elif reports_choice == '8':
                    generate_reports(8)
                elif reports_choice == '9':
                    break
                else:
                    print("Invalid option. Please select a valid option (1-8).")
        elif choice == '5':
            print("Exiting the Wolf Parking Management System. Database connection is closing. Goodbye!")
            # Closing the database connection before leaving
            conn.close()
            break
        else:
            print("Invalid option. Please select a valid option (1/2/3/4/5).")


def main():
    menu()


if __name__ == '__main__':
    main()