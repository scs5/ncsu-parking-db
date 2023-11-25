# This file contains functions for Information Processing
from delete_from_tables import *
from modifyQueries import *
from load_tables import *
import pandas as pd
import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()


# Function requests driver information (name, status, and univeristy ID (or phone numer if they're a visitor)) and adds them to tDrivers
def enter_info_about_drivers():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Enter information about drivers")
    print("Please enter driver status (S = student, E = employee, V = visitor): ")
    status = input()
    if status != "S" and status != "E" and status != "V":
        print("Invalid status provided.")
        return
    if status == "V":
        print("Please enter driver phone number: ")
        u_id = input()
    else:
        print("Please enter driver university ID: ")
        u_id = input()
    print("Please enter driver first and last name: ")
    name = input()
    if u_id == "" or name == "":
        print("Invalid information: you must provide a univeristy ID or phone number and a name.")
        return
    load('tDrivers',[u_id,name,status])
    curs.execute("SELECT * FROM tDrivers;")
    print(curs.fetchall())
    return

# Function requests parking lot information (name and address) and adds it to tLots.
def enter_info_about_parking_lots():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Enter information about parking lots")
    print('Please provide a parking lot name: ')
    l_name = input()
    print('Please provide a lot address: ')
    l_address = input()
    if (l_name == "" or l_address == ""):
        print("Lot name and address are required for this action.")
        return
    load('tLots',[l_name, l_address])
    curs.execute("SELECT * FROM tLots;")
    print(curs.fetchall())
    return

# Function requests zone information (lot name and zoneID) and adds it to tZones.
def enter_info_about_zone():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Enter information about zone")
    print('Please provide an existing parking lot name: ')
    l_name = input()
    print('Please provide a zone ID: ')
    z_ID = input()
    if l_name =="" or z_ID == "":
        print("All data fields are required.")
        return
    load('tZones',[l_name, z_ID])
    return

# Function requests space information (lot and zone names, the number of spots to create, and the types of spaces to make) and adds the spaces to tSpaces
def enter_info_about_spaces(): # DESIGN CHOICE - Not implemented like this yet but we could make it so if we are creating more than one space for a lot at a time, cancel all insertions if one fails
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Enter information about spaces")
    print('Please provide an existing parking lot name: ')
    l_name = input()
    print('Please provide a zone ID within this lot: ')
    z_ID = input()
    if l_name =="" or z_ID =="":
        print('Lot name and zone ID are required fields for this operation.')
        return
    print('If you would like to create multiple spaces in this lot and zone, please type a number. Otherwise, hit enter.')
    num_spaces = input()
    def create_spaces(starting_idx, num = 1):
        for i in range(num):
            load('tSpaces',[l_name, z_ID, starting_idx, space_type, availability])
            starting_idx += 1
    sql  = "SELECT space_number FROM tSpaces WHERE lot_name == '"+l_name+"' AND zoneID == '"+z_ID+"';"
    curs.execute(sql)
    result = curs.fetchall()
    new_space_num = 1
    if len(result) > 0:
        ls = []
        for r in result:
            ls.append(r[0])
        result = ls
        new_space_num = max(result) + 1
    print('Please type one space type for all spaces created at this time. To use "Regular" default, hit enter.')
    space_type = input()
    if space_type == "":
        space_type = 'Regular' # default space type to Null (bc specified w/ other menu item)
    availability = 'Available' # default to true
    if num_spaces == "":
        print('If you would like to create a space with a specific number, please type that space number: ')
        alt = input()
        if alt != "":
            new_space_num = int(alt)
        create_spaces(new_space_num)
    else:
        create_spaces(new_space_num, num = int(num_spaces))
    sql2  = "SELECT space_number FROM tSpaces WHERE lot_name == '"+l_name+"' AND zoneID == '"+z_ID+"';"
    curs.execute(sql2)
    result_final = curs.fetchall()
    print(result_final)
    return

# Function requests permit information to create a permit request in tPermits and tAreAssigned
# the function enforces contrains on the number of permits that are allowed for different types of drivers.
def enter_info_about_permits():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Enter information about permits")
    sql2 = "SELECT * FROM tVehicles;"
    curs.execute(sql2)
    print('FETCHED',curs.fetchall())
    print("Please provide a university ID or phone number: ")
    u_ID = input()
    if u_ID == "":
        print("University ID or phone number is a required field for this operation.")
        return

    sql = "SELECT * FROM tVehicles WHERE license_number IN (SELECT license_number FROM tDrive WHERE univID_phonenumber == '"+u_ID+"');"
    curs.execute(sql)
    print(curs.fetchall())
    print("Please provide the license number of one of your vehicles: ")
    license_num = input()
    if license_num == "":
        print("License number is a required field for this operation.")
        return
    sql2 = "SELECT max(permitID) FROM tPermits;"
    curs.execute(sql2)
    p_ID = curs.fetchone()[0]
    p_ID = str(p_ID+1)
    print('Type a requested permit type: ')
    p_type = input()
    if p_type == "":
        print('Permit type is a required field for this operation.')
        return
    print('Type a requested space type: ')
    s_type = input()
    if s_type == "":
        print("Space type is a required field for this operation.")
        return
    print('Type a requested start date (YYYY-MM-DD): ')
    date = input()
    ls = [p_ID,p_type,s_type]
    if date == "":
        print('Start date is a required field for this action.')
        return
    ls.append(date)
    # expiration date and type default to None since this is part of the permit approval process
    ls.append(None) # for expiration_date
    ls.append(None) # for expiration_time

    # only one active permit request per person at a time
    get_permit_requests = """SELECT * FROM tPermits WHERE permitID IN (SELECT permitID FROM tAreAssigned WHERE univID_phonenumber =="""+u_ID+""") AND expiration_date is NULL;"""
    print(get_permit_requests)
    curs.execute(get_permit_requests)
    permit_requests = curs.fetchall()
    print('PERMIT REQUESTS:',permit_requests)
    if len(permit_requests)>0:
        print("You already have an active permit request. Please wait for your permit to be approved or denied before making an additional request.")
        return
    # allow citation request (or prevent request) depending on the existing permits and the driver's status
    check_status = "SELECT status FROM tDrivers WHERE univID_phonenumber =='"+u_ID+"';"
    curs.execute(check_status)
    status = curs.fetchone()
    if (status == None):
        print("Error: University ID was not recognized.")
        return
    status = status[0]
    print('STATUS:',status)
    get_permits = """SELECT * FROM tPermits WHERE permitID IN (SELECT permitID FROM tAreAssigned WHERE univID_phonenumber =="""+u_ID+""") AND start_date<= DATE('"""+date+"""') AND expiration_date>= DATE('"""+date+"""');"""
    print(get_permits)
    curs.execute(get_permits)
    permits = curs.fetchall()
    print('PERMITS:',permits)
    if len(permits)>0:
        if status == "V":
            print("Visitors cannot have more than 1 valid permits at a time.")
            return
        types = [p[1] for p in permits]
        print("TYPES:", types)
        if (len(permits) == 2 and status == "S") or (len(permits) == 3 and status == "E"):
            print("Maximum number of permits has already been reached.")
            return
        # if the have a non-park&ride or special event permit, they can only add special event or park & ride permit
        if ('Special Event' not in permits) and ('Park & Ride' not in permits):
            if status == "S":
                if (p_type != 'Special Event') and (p_type != 'Park & Ride'):
                    print('You already hold a Residential, Commuter, or Peak Hours permit. You may only request a special event or park & ride permit for this start date.')
                    return
            if status == "E" and len(permits)==2:
                if (p_type != 'Special Event') and (p_type != 'Park & Ride'):
                    print('You already hold 2 permits of types Residential, Commuter, or Peak Hours permit. You may only request a special event or park & ride permit for this start date.')
                    return
    try:
        curs.execute("BEGIN TRANSACTION;")
        insert_sql = "INSERT INTO tPermits VALUES (?,?,?,?,?,?);"
        curs.execute(insert_sql,ls)
        insert_sql2 = "INSERT INTO tAreAssigned VALUES (?,?);"
        curs.execute(insert_sql2,[u_ID,p_ID])
        insert_sql3 = "INSERT INTO tAreAssociatedWith VALUES (?,?);"
        curs.execute(insert_sql3,[license_num,p_ID])
        curs.execute("COMMIT;")
        print('Permit successfully created.')
    except:
        print('failure')
        curs.execute("ROLLBACK;")
    return

# Function requests driver univeristy ID or phone number to update any or all driver information
def update_info_about_drivers():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Update information about drivers")
    print('Please provide a university ID or phone number: ')
    u_id = input()
    if u_id == "":
        print("University ID is a required field for this operation.")
        return
    sql1= "SELECT * FROM tDrivers WHERE univID_phonenumber =="+u_id+";"
    curs.execute(sql1)
    out1 = curs.fetchall()
    print("Current driver information", out1)
    if len(out1) == 0:
        print("No such driver found with university ID or phone number "+u_id)
        # print("(1) Go back to information processing menu")
        # go_back_choice = input()
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

# Function requests lot name and allows user to update lot name and/or address
def update_info_about_parking_lots():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Update information about parking lots")
    print("Type an existing parking lot name: ")
    old_name = input()
    if old_name == "":
        print("You must provide a parking lot name to proceed.")
        return
    print("To leave any data field unchanged, press enter when prompted to suply that information.")
    print("Type updated parking lot name: ")
    new_name = input()
    print("Type updated address: ")
    new_address = input()
    if new_name == new_address == "":
        print('No update made to lot information.')
        return

    # Making sure the permit we are about to update exists
    sqlQ = "SELECT * FROM tLots WHERE lot_name == '"+old_name+"';"
    curs.execute(sqlQ)
    result = curs.fetchall()
    if len(result) == 0: # Making sure the old lot exists
        print('No lot with this name found.')
        return

    sqlQ = "SELECT * FROM tLots WHERE lot_name == '"+old_name+"';"
    curs.execute(sqlQ)
    result = curs.fetchall()[0]
    print(result)
    if new_name == "":
        new_name = result[0]
    if new_address == "":
        new_address = result[1]
    updateParkingLotInfo(old_name,new_name,new_address)
    return

# Function requests zone ID to update information on that zone within all lots OR within a specific lot
def update_info_about_zone():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Update information about zone")
    print("(1) Change the zone ID of a zone across all lots.")
    print("(2) Change the zone ID of a zone in a specific lot.")
    update_info_about_zone_choice = input()
    print("Please type an existing zone ID: ")
    z_ID = input()
    print("Please type an updated zone ID: ")
    z_ID_new = input()
    if update_info_about_zone_choice == "2":
        print("Please type an existing lot name: ")
        l_name = input()
        updateZone(l_name,z_ID,z_ID_new)
        return
    else:
        # print("OPTION 1",z_ID_new)
        sql = "SELECT DISTINCT lot_name FROM tZones WHERE zoneID == '"+z_ID+"';"
        curs.execute(sql)
        lots = [l[0] for l in curs.fetchall()]
        print(lots)
        if len(lots)==0:
            print("No lots with this zone ID exist.")
            return
        for lot in lots:
            print(lot)
            updateZone(lot,z_ID,z_ID_new)
        print('Zone information for lot '+str(lots)+' updated.')
        return

# Function requests lot name, zone ID, and lot name to allow updates to all
# information about a space within a specific lot and zone (space # cannot be updated)
def update_info_about_spaces():
    curs.execute("PRAGMA foreign_keys = ON;")
    # update or set space type or update availability
    print("You selected Update information about spaces")
    print("Please type an existing lot name: ")
    l_name = input()
    print("Please type an existing zone ID: ")
    z_ID = input()
    print("Please type an existing space number: ")
    s_number = input()
    if l_name == "" or s_number == "" or z_ID == "":
        print('Lot name, zone ID, and space number must be provided.')
        return
    sql = "SELECT * FROM tSpaces WHERE lot_name == '"+l_name+"' AND zoneID == '"+z_ID+"' AND space_number =="+s_number+";"
    curs.execute(sql)
    spaces = curs.fetchall()
    print(spaces)
    print("To leave any data field unchanged, press enter when prompted to suply that information.")
    print("Please type an updated space type: ")
    type = input()
    print("Please type an updated space availability: ")
    availability = input()
    if type == availability == "":
        print('No changes to spaces made.')
        return
    else:
        if type == "":
            type = spaces[0][3]
            print(type)
        if availability == "":
            availability = spaces[0][4]
            print(availability)
        updateSpace(s_number,l_name,z_ID,availability,type)
        sql2 = "SELECT * FROM tSpaces WHERE lot_name == '"+l_name+"' AND zoneID == '"+z_ID+"' AND space_number =="+s_number+";"
        curs.execute(sql2)
        result = curs.fetchall()
        print(result)
        return

# Function requests driver univ ID or phone number and removes the driver from tDrivers.
# The delete cascades to all relevant tables.
def delete_info_about_drivers():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Delete information about drivers")
    print("Please type a driver's univeristy ID or phone number.")
    u_ID = input()
    if u_ID == "":
        print('University ID or phone number is a required field.')
        return
    sql = "SELECT * FROM tDrivers WHERE univID_phonenumber =="+u_ID+";"
    print(sql)
    curs.execute(sql)
    result = curs.fetchall()
    if len(result) == 0:
        print('No drivers with this univeristy ID or phone number found.')
        return
    delete_driver(u_ID)
    print("Done.")
    return

# Function requests parking lot name and removes this lot from tLots.
# Delete cascades to relevant tables (namely the zones and spaces of this lot are deleted)
def delete_info_about_parking_lots():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Delete information about parking lots")
    print("Please type the name of an existing lot: ")
    l_name = input()
    if l_name == "":
        print("Lot name is a required field for this action.")
        return
    sql = "SELECT * FROM tLots WHERE lot_name =='"+l_name+"';"
    curs.execute(sql)
    print('Before:', curs.fetchall())
    delete_lot(l_name)
    curs.execute(sql)
    print('After:',curs.fetchall())
    return

# Function requests zone ID and deletes this zone from all lots containing this zone.
# Delete casecades to all relevant tables (namely the spaces in this zone are deleted).
def delete_info_about_zone():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Delete information about zone")
    print("Please type an existing zone ID: ")
    z_ID = input()
    if z_ID == "":
        print("Zone ID is a required field for this action.")
        return
    print("Would you like to delete this zone from all lots or within a specific lot?")
    print("(1) Delete zone from all lots")
    print("(2) Delete zone from a specific lot")
    choice1 = input()
    if choice1 != "1" and choice1 != "2":
        return
    sql = "SELECT * FROM tZones WHERE zoneID =='"+z_ID+"';"
    curs.execute(sql)
    print('Before:', curs.fetchall())
    if choice1 == "1":
        delete_zone(z_ID)
    if choice1 == "2":
        print("Please type an existing lot name:")
        l_name = input()
        delete_zone(lot_name = l_name, zoneID = z_ID)
    else:
        print("ELSE!!!")
    curs.execute(sql)
    print('After:',curs.fetchall())

    sql = "SELECT * FROM tZones;"
    curs.execute(sql)
    print(curs.fetchall())
    return

# Function requests space number, zone ID, and Lot name to delete a specific space from tLots
# Delete doesn't effect other spaces with this number in different zones and/or lots
def delete_info_about_spaces():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Delete information about spaces")
    print("Please type an existing lot name: ")
    l_name = input()
    print("Please type an existing zone ID: ")
    z_ID = input()
    print("Please type an existing space number in this lot.")
    space_number = input()
    if l_name == "" or z_ID == "" or space_number == "":
        print("Lot name, zone ID, and space number are all required fields for this operation.")
        return
    sql = "SELECT * FROM tSpaces WHERE lot_name =='"+l_name+"' AND zoneID =='"+z_ID+"' AND space_number =="+space_number+";"
    print(sql)
    curs.execute(sql)
    print(curs.fetchall())
    delete_space(l_name,z_ID,space_number)
    curs.execute(sql)
    print(curs.fetchall())
    sql1 = "SELECT * FROM tSpaces;"
    curs.execute(sql1)
    print(curs.fetchall())
    return

# Function requests permit ID (and allows you to look up the permit Id you want using univeristy ID or phone number)
# Deletes the permit from tPermits.
def delete_info_about_permits():
    curs.execute("PRAGMA foreign_keys = ON;")
    print("You selected Delete information about permits")
    print("(1) Look up permit ID using univeristy ID or phone number")
    print("(2) Delete permit using permit ID")
    delete_info_about_permits_choice = input()
    if delete_info_about_permits_choice=="1":
        print("Please type a univeristy ID or phonenumber: ")
        u_ID = input()
        if u_ID == "":
            sql = "SELECT * FROM tAreAssigned;"
            curs.execute(sql)
            print(curs.fetchall())
            sql = "SELECT * FROM tPermits;"
            curs.execute(sql)
            print(curs.fetchall())
            return
        sql ="SELECT * FROM tAreAssigned WHERE univID_phonenumber == '"+u_ID+"';"
        curs.execute(sql)
        print('Permit IDs associated with driver: ',curs.fetchall())
        return
    elif delete_info_about_permits_choice =="2":
        print("Please type an existing permit ID:")
        p_ID = input()
        if p_ID == "":
            print("Permit ID is a required field for this action.")
            return
        delete_permit(p_ID)
        sql = "SELECT * FROM tPermits WHERE permitID =="+p_ID+";"
        curs.execute(sql)
        print(curs.fetchall())
        return
    else:
        return
