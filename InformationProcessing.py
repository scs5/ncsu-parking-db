# This file contains functions for Information Processing
from modifyQueries import *
from load_tables import *
import pandas as pd
import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()

def enter_info_about_drivers():
    print("You selected Enter information about drivers")
    print("Please enter driver status (S = student, E = employee, V = visitor): ")
    status = input()
    if status == "V":
        print("Please enter driver phone number: ")
        u_id = input()
    else:
        print("Please enter driver university ID: ")
        u_id = input()
    print("Please enter driver first and last name: ")
    name = input()
    if u_id == "":
        print("Invalid information: you must provide a univeristy ID or phone number")
        return
    load('tDrivers',[u_id,name,status])
    curs.execute("SELECT * FROM tDrivers;")
    print(curs.fetchall())
    return


def enter_info_about_parking_lots():
    print("You selected Enter information about parking lots")
    print('Please provide a lot name: ')
    l_name = input()
    print('Please provide a lot address: ')
    l_address = input()
    load('tLots',[l_name, l_address])
    curs.execute("SELECT * FROM tLots;")
    print(curs.fetchall())
    return

def enter_info_about_zone():
    print("You selected Enter information about zone")
    print('Please provide an existing lot name: ')
    l_name = input()
    print('Please provide a zone ID: ')
    z_ID = input()
    load('tZones',[l_name, z_ID])
    return

def enter_info_about_spaces(l_name):
    print("You selected Enter information about spaces")

def enter_info_about_permits(u_id):
    print("You selected Enter information about permits")

def update_info_about_drivers(u_id):
    print("You selected Update information about drivers")
    sql1= "SELECT * FROM tDrivers WHERE univID_phonenumber =="+u_id+";"
    curs.execute(sql1)
    out1 = curs.fetchall()
    print("Current driver information", out1)
    if len(out1) == 0:
        print("No such driver found with university ID or phone number "+u_id)
        print("(1) Go back to information processing menu")
        go_back_choice = input()
        return
    sql2= "SELECT * FROM tVehicles WHERE license_number IN (SELECT license_number FROM tDrive WHERE univID_phonenumber=="+u_id+");"
    curs.execute(sql2)
    out2 = curs.fetchall()
    print("Current vehicle information", out2)
    print("\n(1) Update driver information")
    enter_info_about_drivers_choice = input()
    if enter_info_about_drivers_choice == "1":
        # ID = sql1[0][0]
        name = out1[0][1]
        status = out1[0][2]
        print("To leave any data field unchanged, press enter when prompted to suply that information.")
        # print("Type driver university ID or phone number: ")
        # d_ID = input()
        print("Type updated driver name: ")
        d_name = input()
        print("Type updated driver status: ")
        d_status = input()
        if d_name == d_status == "":
            print("Driver information not modified")
            return
        if d_name == "":
            d_name = name
        if d_status == "":
            d_status = status
        updateDriverInfo(u_id, d_name, d_status)
        curs.execute(sql1)
        out1_updated = curs.fetchall()
        print(out1_updated)
        return
def update_info_about_parking_lots(l_name):
    print("You selected Update information about parking lots")

def update_info_about_zone(z_ID):
    print("You selected Update information about zone")

def update_info_about_spaces(l_name,s_number):
    # update or set space type or update availability
    print("You selected Update information about spaces")

def update_info_about_permits(u_id):
    print("You selected Update information about permits")

def delete_info_about_drivers(u_id):
    print("You selected Delete information about drivers")

def delete_info_about_parking_lots(l_name):
    print("You selected Delete information about parking lots")

def delete_info_about_zone(z_ID):
    print("You selected Delete information about zone")

def delete_info_about_spaces(l_name,s_number):
    print("You selected Delete information about spaces")

def delete_info_about_permits(u_id):
    print("You selected Delete information about permits")

def assign_zones_to_parking_lots(l_name):
    print("You selected Assign zones to each parking lot")

# def assign_type_to_space():
#     print("You selected Assign a type to a given space")

def request_citation_appeals():
    print("You selected Request Citation Appeals")

def approve_citation_appeals():
    print("You selected Approve Citation Appeals")


# conn.close()
