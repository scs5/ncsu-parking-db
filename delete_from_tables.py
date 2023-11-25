import sqlite3 as sql
conn = sql.connect('parking.db')
curs = conn.cursor()
curs.execute("PRAGMA foreign_keys = ON;")


# tDrivers
def delete_driver(univID_phonenumber=None, name=None, status=None):
    if univID_phonenumber or name or status:
        query = "DELETE FROM tDrivers WHERE "
        conditions = []
        if univID_phonenumber:
            conditions.append(f"univID_phonenumber == {univID_phonenumber}")
        if name:
            conditions.append(f"name == '{name}'")
        if status:
            conditions.append(f"status == '{status}'")
        query += " AND ".join(conditions) + ";"
        print(query)
        curs.execute(query)
        conn.commit()


# tVehicles
def delete_vehicle(license_number=None, model=None, color=None, manufacturer=None, year=None):
    if license_number or model or color or manufacturer or year:
        query = "DELETE FROM tVehicles WHERE "
        conditions = []
        if license_number:
            conditions.append(f"license_number == '{license_number}'")
        if model:
            conditions.append(f"model == '{model}'")
        if color:
            conditions.append(f"color == '{color}'")
        if manufacturer:
            conditions.append(f"manufacturer == '{manufacturer}'")
        if year:
            conditions.append(f"year == {year}")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tDrive
def delete_drive(license_number=None, univID_phonenumber=None):
    if license_number or univID_phonenumber:
        query = "DELETE FROM tDrive WHERE "
        conditions = []
        if license_number:
            conditions.append(f"license_number == '{license_number}'")
        if univID_phonenumber:
            conditions.append(f"univID_phonenumber == {univID_phonenumber}")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tPermits
def delete_permit(permitID=None, permit_type=None, space_type=None):
    if permitID or permit_type or space_type:
        query = "DELETE FROM tPermits WHERE "
        conditions = []
        if permitID:
            conditions.append(f"permitID == {permitID}")
        if permit_type:
            conditions.append(f"permit_type == '{permit_type}'")
        if space_type:
            conditions.append(f"space_type == '{space_type}'")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        print(query)
        conn.commit()


# tAreAssigned
def delete_assigned(univID_phonenumber=None, permitID=None):
    if univID_phonenumber or permitID:
        query = "DELETE FROM tAreAssigned WHERE "
        conditions = []
        if univID_phonenumber:
            conditions.append(f"univID_phonenumber == {univID_phonenumber}")
        if permitID:
            conditions.append(f"permitID == {permitID}")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tAreAssociatedWith
def delete_associated(license_number=None, permitID=None):
    if license_number or permitID:
        query = "DELETE FROM tAreAssociatedWith WHERE "
        conditions = []
        if license_number:
            conditions.append(f"license_number == '{license_number}'")
        if permitID:
            conditions.append(f"permitID == {permitID}")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tLots
def delete_lot(lot_name=None, address=None):
    if lot_name or address:
        query = "DELETE FROM tLots WHERE "
        conditions = []
        if lot_name:
            conditions.append(f"lot_name == '{lot_name}'")
        if address:
            conditions.append(f"address == '{address}'")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tZones
def delete_zone(zoneID=None,lot_name=None):
    if lot_name or zoneID:
        query = "DELETE FROM tZones WHERE "
        conditions = []
        if lot_name:
            conditions.append(f"lot_name == '{lot_name}'")
        if zoneID:
            conditions.append(f"zoneID == '{zoneID}'")
        query += " AND ".join(conditions) + ";"
        print(query)
        curs.execute(query)
        conn.commit()


# tAllowsDriverToParkIn
def delete_allowed(permitID=None, zoneID=None, lot_name=None):
    if permitID or zoneID or lot_name:
        query = "DELETE FROM tAllowsDriverToParkIn WHERE "
        conditions = []
        if permitID:
            conditions.append(f"permitID == {permitID}")
        if zoneID:
            conditions.append(f"zoneID == '{zoneID}'")
        if lot_name:
            conditions.append(f"lot_name == '{lot_name}'")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tSpaces
def delete_space(lot_name=None, zoneID=None, space_number=None):
    if lot_name or zoneID or space_number:
        query = "DELETE FROM tSpaces WHERE "
        conditions = []
        if lot_name:
            conditions.append(f"lot_name == '{lot_name}'")
        if zoneID:
            conditions.append(f"zoneID == '{zoneID}'")
        if space_number:
            conditions.append(f"space_number == {space_number}")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tCitations
def delete_citation(citation_number=None, category=None, citation_date=None, citation_time=None):
    if citation_number or category or citation_date or citation_time:
        query = "DELETE FROM tCitations WHERE "
        conditions = []
        if citation_number:
            conditions.append(f"citation_number == {citation_number}")
        if category:
            conditions.append(f"category == '{category}'")
        if citation_date:
            conditions.append(f"citation_date == '{citation_date}'")
        if citation_time:
            conditions.append(f"citation_time == '{citation_time}'")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tAreTicketedTo
def delete_ticketed(license_number=None, citation_number=None):
    if license_number or citation_number:
        query = "DELETE FROM tAreTicketedTo WHERE "
        conditions = []
        if license_number:
            conditions.append(f"license_number == '{license_number}'")
        if citation_number:
            conditions.append(f"citation_number == {citation_number}")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


# tAreIssuedWithin
def delete_issued(lot_name=None, citation_number=None):
    if lot_name or citation_number:
        query = "DELETE FROM tAreIssuedWithin WHERE "
        conditions = []
        if lot_name:
            conditions.append(f"lot_name == '{lot_name}'")
        if citation_number:
            conditions.append(f"citation_number == {citation_number}")
        query += " AND ".join(conditions) + ";"
        curs.execute(query)
        conn.commit()


def run_examples():
    # Examples
    delete_driver(univID_phonenumber='123456', name='John Doe')
    delete_vehicle(license_number='ABC123', model='Sedan')
    delete_drive(license_number='XYZ789')
    delete_permit(permitID=1)
    delete_assigned(univID_phonenumber='123456')
    delete_associated(license_number='XYZ789')
    delete_lot(lot_name='Parking Lot A')
    delete_zone(lot_name='Parking Lot A', zoneID='Zone1')
    delete_allowed(permitID=1)
    delete_space(lot_name='Parking Lot A', zoneID='Zone1', space_number=101)
    delete_citation(citation_number=1)
    delete_ticketed(license_number='ABC123', citation_number=1)
    delete_issued(lot_name='Parking Lot A', citation_number=1)


if __name__ == '__main__':
    run_examples()
