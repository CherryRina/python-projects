#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from datetime import datetime, timedelta

# setup flight search
data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_destination_data()
ORIGIN_CITY_IATA = "TLV"

# add city code if empty
if sheet_data[0]["iataCode"] == '':
    print("the iataCode is empty")
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(city=row["city"])
    # update the sheet with new code 
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

# define flight time
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# get flight offers
for row in sheet_data:
    # get all flights offers
    all_flights_for_row = flight_search.get_flight_offers(
        origin_city_code=ORIGIN_CITY_IATA, 
        destination_city_code=row["iataCode"],
        from_time=tomorrow
        #to_time=six_month_from_today
    )
    # finds cheapest one
    cheapest_flight = FlightData.find_cheapest_flight(all_flights_for_row) # FlightData object
    print(f"{row["city"]} result: {cheapest_flight.price}$")



"""
tomorrow:
- check the second date
- debug the program 
"""