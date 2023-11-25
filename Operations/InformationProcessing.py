from utils import *
import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()
curs.execute("PRAGMA foreign_keys = ON;")


def enter_info_about_drivers():
    """ Add a driver to the database. """

    # User enters driver status
    print("Please enter driver status (S = student, E = employee, V = visitor): ")
    status = input()
    # Error handling
    if status != "S" and status != "E" and status != "V":
        print("Invalid status provided.")
        return
    
    # User enters driver ID or phone number
    if status == "V":
        print("Please enter driver phone number: ")
        u_id = input()
    else:
        print("Please enter driver university ID: ")
        u_id = input()

    # User enters driver name
    print("Please enter driver first and last name: ")
    name = input()
    if u_id == "" or name == "":
        print("Invalid information: you must provide a univeristy ID or phone number and a name.")
        return
    
    # Execute SQL
    load('tDrivers',[u_id,name,status])
    curs.execute("SELECT * FROM tDrivers;")


def enter_info_about_parking_lots():
    """ Add a parking lot to the database. """

    # User enters parking lot name and address
    print('Please provide a parking lot name: ')
    l_name = input()
    print('Please provide a lot address: ')
    l_address = input()
    
    # Error handling
    if (l_name == "" or l_address == ""):
        print("Lot name and address are required for this action.")
        return
    
    # Execute SQL
    load('tLots',[l_name, l_address])
    curs.execute("SELECT * FROM tLots;")


def enter_info_about_zone():
    """ Add a zone to the database. """

    # User enters parking lot name and zone ID
    print('Please provide an existing parking lot name: ')
    l_name = input()
    print('Please provide a zone ID: ')
    z_ID = input()

    # Error handling
    if l_name =="" or z_ID == "":
        print("All data fields are required.")
        return
    
    # Execute SQL
    load('tZones',[l_name, z_ID])


def enter_info_about_spaces():
    """ Add parking spaces to the database. """

    # User enters parking lot name and zone ID
    print('Please provide an existing parking lot name: ')
    l_name = input()
    print('Please provide a zone ID within this lot: ')
    z_ID = input()

    # Error handling
    if l_name =="" or z_ID =="":
        print('Lot name and zone ID are required fields for this operation.')
        return
    
    # User adds either a single space or multiple spaces
    print('If you would like to create multiple spaces in this lot and zone, please type a number. Otherwise, hit enter.')
    num_spaces = input()
    def create_spaces(starting_idx, num = 1):
        for i in range(num):
            load('tSpaces',[l_name, z_ID, starting_idx, space_type, availability])
            starting_idx += 1

    # Execute SQL to fetch current spaces to increment from
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

    # User enters type of space
    print('Please type one space type for all spaces created at this time. To use "Regular" default, hit enter.')
    space_type = input()
    if space_type == "":
        space_type = 'Regular'
    availability = 'Available' # default to available

    # User enters space number
    if num_spaces == "":
        print('If you would like to create a space with a specific number, please type that space number: ')
        alt = input()
        if alt != "":
            new_space_num = int(alt)
        create_spaces(new_space_num)
    else:
        create_spaces(new_space_num, num = int(num_spaces))


def enter_info_about_permits():
    """ Add a permit to the database. """

    # User enter driver ID or phone number
    print("Please provide a university ID or phone number: ")
    u_ID = input()
    if u_ID == "":
        print("University ID or phone number is a required field for this operation.")
        return


    # User enters license plate number
    print("Please provide the license number of one of your vehicles: ")
    license_num = input()
    if license_num == "":
        print("License number is a required field for this operation.")
        return
    
    # Fetch new permit ID
    sql2 = "SELECT max(permitID) FROM tPermits;"
    curs.execute(sql2)
    p_ID = curs.fetchone()[0]
    p_ID = str(p_ID+1)

    # User enters requested permit type
    print('Type a requested permit type: ')
    p_type = input()
    if p_type == "":
        print('Permit type is a required field for this operation.')
        return
    
    # User enters requested space type
    print('Type a requested space type: ')
    s_type = input()
    if s_type == "":
        print("Space type is a required field for this operation.")
        return
    
    # User enters requested start date
    print('Type a requested start date (YYYY-MM-DD): ')
    date = input()
    ls = [p_ID,p_type,s_type]
    if date == "":
        print('Start date is a required field for this action.')
        return
    
    # Expiration date and time are None for unapproved permits
    ls.append(date)
    ls.append(None)
    ls.append(None)

    # Only one active permit request per person at a time
    get_permit_requests = """SELECT * FROM tPermits WHERE permitID IN (SELECT permitID FROM tAreAssigned WHERE univID_phonenumber =="""+u_ID+""") AND expiration_date is NULL;"""
    curs.execute(get_permit_requests)
    permit_requests = curs.fetchall()
    print('PERMIT REQUESTS:',permit_requests)
    if len(permit_requests)>0:
        print("You already have an active permit request. Please wait for your permit to be approved or denied before making an additional request.")
        return
    
    # Allow citation request (or prevent request) depending on the existing permits and the driver's status
    check_status = "SELECT status FROM tDrivers WHERE univID_phonenumber =='"+u_ID+"';"
    curs.execute(check_status)
    status = curs.fetchone()
    if (status == None):
        print("Error: University ID was not recognized.")
        return
    status = status[0]

    get_permits = """SELECT * FROM tPermits WHERE permitID IN (SELECT permitID FROM tAreAssigned WHERE univID_phonenumber =="""+u_ID+""") AND start_date<= DATE('"""+date+"""') AND expiration_date>= DATE('"""+date+"""');"""
    curs.execute(get_permits)
    permits = curs.fetchall()
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


def update_info_about_drivers():
    """ Update information about a driver. """

    # User enters driver ID or phone number
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
        return
    
    # User enters vehicle information
    sql2= "SELECT * FROM tVehicles WHERE license_number IN (SELECT license_number FROM tDrive WHERE univID_phonenumber=="+u_id+");"
    curs.execute(sql2)
    out2 = curs.fetchall()
    print("Current vehicle information", out2)
    print("\n(1) Update driver information")
    enter_info_about_drivers_choice = input()
    if enter_info_about_drivers_choice == "1":
        # User enters updated information
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

        # Execute SQL
        updateDriverInfo(u_id, d_name, d_status)


def update_info_about_parking_lots():
    """ Update information about parking lots.  """

    # User enters parking lot name
    print("Type an existing parking lot name: ")
    old_name = input()
    if old_name == "":
        print("You must provide a parking lot name to proceed.")
        return
    
    # User enters updated information
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
    if len(result) == 0:
        print('No lot with this name found.')
        return

    # Execute SQL
    if new_name == "":
        new_name = result[0]
    if new_address == "":
        new_address = result[1]
    updateParkingLotInfo(old_name,new_name,new_address)


def update_info_about_zone():
    """ Update information about zones. """

    # User chooses bulk update or specific update
    print("(1) Change the zone ID of a zone across all lots.")
    print("(2) Change the zone ID of a zone in a specific lot.")
    update_info_about_zone_choice = input()

    # User enters updated information
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


def update_info_about_spaces():
    """ Update information about spaces. """

    # User select space to update
    print("Please type an existing lot name: ")
    l_name = input()
    print("Please type an existing zone ID: ")
    z_ID = input()
    print("Please type an existing space number: ")
    s_number = input()
    if l_name == "" or s_number == "" or z_ID == "":
        print('Lot name, zone ID, and space number must be provided.')
        return
    
    # User enters updated information
    sql = "SELECT * FROM tSpaces WHERE lot_name == '"+l_name+"' AND zoneID == '"+z_ID+"' AND space_number =="+s_number+";"
    curs.execute(sql)
    spaces = curs.fetchall()
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


def delete_info_about_drivers():
    """ Delete driver from database. """

    # User enters driver ID or phone number
    print("Please type a driver's univeristy ID or phone number.")
    u_ID = input()
    if u_ID == "":
        print('University ID or phone number is a required field.')
        return
    sql = "SELECT * FROM tDrivers WHERE univID_phonenumber =="+u_ID+";"
    curs.execute(sql)
    result = curs.fetchall()
    if len(result) == 0:
        print('No drivers with this univeristy ID or phone number found.')
        return
    
    # Execute SQL
    delete_driver(u_ID)


def delete_info_about_parking_lots():
    """ Delete parking lot from database. """

    # User enters parking lot name
    print("Please type the name of an existing lot: ")
    l_name = input()
    if l_name == "":
        print("Lot name is a required field for this action.")
        return
    
    # Execute SQL
    delete_lot(l_name)


def delete_info_about_zone():
    """ Delete zone from database. """

    # User enters zone ID
    print("Please type an existing zone ID: ")
    z_ID = input()
    if z_ID == "":
        print("Zone ID is a required field for this action.")
        return
    
    # User can either bulk delete or specific delete
    print("Would you like to delete this zone from all lots or within a specific lot?")
    print("(1) Delete zone from all lots")
    print("(2) Delete zone from a specific lot")
    choice1 = input()
    if choice1 != "1" and choice1 != "2":
        return
    if choice1 == "1":
        delete_zone(z_ID)
    if choice1 == "2":
        print("Please type an existing lot name:")
        l_name = input()
        delete_zone(lot_name = l_name, zoneID = z_ID)


def delete_info_about_spaces():
    """ Delete spaces from database. """
    
    # User enters space information
    print("Please type an existing lot name: ")
    l_name = input()
    print("Please type an existing zone ID: ")
    z_ID = input()
    print("Please type an existing space number in this lot.")
    space_number = input()
    if l_name == "" or z_ID == "" or space_number == "":
        print("Lot name, zone ID, and space number are all required fields for this operation.")
        return

    # Execute SQL
    delete_space(l_name,z_ID,space_number)


def delete_info_about_permits():
    """ Delete permit from database. """
    
    # User can look up permit or delete one
    print("(1) Look up permit ID using univeristy ID or phone number")
    print("(2) Delete permit using permit ID")
    delete_info_about_permits_choice = input()

    # Look up permit IDs
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
    
    # Delete permit
    elif delete_info_about_permits_choice =="2":
        print("Please type an existing permit ID:")
        p_ID = input()
        if p_ID == "":
            print("Permit ID is a required field for this action.")
            return
        delete_permit(p_ID)