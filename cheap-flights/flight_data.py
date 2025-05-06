class FlightData:
    #This class is responsible for structuring the flight data.
    
    def __init__(self, price, origin_airport, destination_airport, out_date):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date

    @staticmethod
    def find_cheapest_flight(flights_data):
        """ 
        function: finds the cheapest flight
        returns: FlightData object
        """
        
        # checks for errors - returns N/A if found
        if flights_data is None or not flights_data['data']:
            print("No flight data")
            return FlightData("N/A", "N/A", "N/A", "N/A")
        # create the first flight object
        firts_flight = flights_data["data"][0]
        lowest_price = float(firts_flight["price"]["grandTotal"])
        origin = firts_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        destination = firts_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
        out_date = firts_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
        cheapest_flight = FlightData(
            price=lowest_price, 
            origin_airport=origin, 
            destination_airport=destination, 
            out_date=out_date        )
        # find the lowest price
        if flights_data != []:
            for flight in flights_data["data"]:
                flights_price = float(flight["price"]["grandTotal"])
                if flights_price < lowest_price:
                    lowest_price = flights_price
                    cheapest_flight = FlightData(
                        price=float(flight["price"]["grandTotal"]),
                        origin_airport=flight["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                        destination_airport=flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"],
                        out_date=flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
                    )
                    print(f"cheapest flight to {destination} is {lowest_price}$")
        return cheapest_flight