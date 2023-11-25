import pandas as pd
from load_tables import *
from create_tables import *
from drop_tables import *

def load_demo_data():
    # Reset database
    drop_tables()
    create_tables()

    # Load driver data
    driver_data = pd.read_csv('./demo-data/drivers.csv')
    load('tDrivers', driver_data, option = 1, type = "bulk", demo=True)

    # Load parking lot data
    lot_data = pd.read_csv('./demo-data/parkinglots.csv')
    load('tLots', lot_data, option = 1, type = "bulk", demo=True)

    # Load vehicle data
    vehicle_data = pd.read_csv('./demo-data/vehicles.csv')
    load('tVehicles', vehicle_data, option = 1, type = "bulk", demo=True)

    # Load drive relation data
    drive_data = pd.DataFrame({
        'license_number': vehicle_data['license_number'],
        'univID_phonenumber': driver_data['univID_phonenumber']
    })
    load('tDrive', drive_data, option = 1, type = "bulk", demo=True)

    # Load permit data
    permit_data = pd.read_csv('./demo-data/permits.csv')
    assigned_to_data = pd.DataFrame({
        'univID_phonenumber': driver_data['univID_phonenumber'],
        'permitID': range(1, 7)
    })
    vehicle_data.drop(vehicle_data.index[-1], inplace=True)
    associated_with_data = pd.DataFrame({
        'license_number': vehicle_data['license_number'],
        'permitID': range(1, 7)
    })
    updated_permit_data = permit_data.drop(['permitID', 'zoneID', 'univID_phonenumber'], axis=1)
    print(updated_permit_data)
    load('tPermits', updated_permit_data, option = 1, type = "bulk", demo=True)
    load('tAreAssociatedWith', associated_with_data, option = 1, type = "bulk", demo=True)
    load('tAreAssigned', assigned_to_data, option = 0, type = "bulk", demo=True)

    # Load zone data
    zone_data = pd.DataFrame({
        'lot_name': ['Poulton Deck', 'Poulton Deck', 'Partners Way Deck',   # made this up -- not included in demo data
                     'Dan Allen Parking Deck', 'Poulton Deck', 'Partners Way Deck'],
        'zoneID': permit_data['zoneID']
    })
    load('tZones', zone_data, option = 1, type = "bulk", demo=True)

    # Load permit-zone relation data
    allows_drivers_data = pd.DataFrame({
        'permitID': [5, 2, 3, 4, 1, 6],
        'zoneID': zone_data['zoneID'],
        'lot_name': zone_data['lot_name']
    })
    print(allows_drivers_data)
    load('tAllowsDriverToParkIn', allows_drivers_data, option = 0, type = "bulk", demo=True)

    # Load citation data
    citation_data = pd.read_csv('./demo-data/citations.csv')
    ticketed_to_data = citation_data[['license_number', 'citation_number']]
    issued_within_data = citation_data[['lot_name', 'citation_number']]
    citation_data = citation_data[['citation_number', 'category', 'citation_date', 'citation_time', 'fee', 'payment_status']]
    citation_data = citation_data.drop('citation_number', axis=1)
    load('tCitations', citation_data, option = 0, type = "bulk", demo=True)
    load('tAreTicketedTo', ticketed_to_data, option = 1, type = "bulk", demo=True)
    load('tAreIssuedWithin', issued_within_data, option = 1, type = "bulk", demo=True)
    return

load_demo_data()
# if __name__ == '__main__':
#     load_demo_data()
#     conn.close()
