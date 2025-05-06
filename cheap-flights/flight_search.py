import os
import requests
import json
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

# env var
AMADEUS_TOKEN_ENDPOINT = 'https://test.api.amadeus.com/v1/security/oauth2/token'
AMADEUS_CITIES_SEARCH_ENDPOINT = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
AMADEUS_FLIGHT_OFFERS_ENDPOINT = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()
    
    def _get_new_token(self):
        """ function returns the token for amadeus """
        headers = {
            "content-type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        response = requests.post(
            url=AMADEUS_TOKEN_ENDPOINT, 
            headers=headers, 
            data=body)
        token = response.json()["access_token"]
        return(token)
    
    def get_destination_code(self, city):
        """ function recieves a city name and returns its iata code """
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(
            url=AMADEUS_CITIES_SEARCH_ENDPOINT, 
            headers=headers, 
            params=query
            )
        code = response.json()["data"][0]['iataCode']
        return code
    
    def get_flight_offers(self, origin_city_code, destination_city_code, from_time):
        """ method finds all flight offers """
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            #"returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "max": "200"
        }
        response = requests.get(
            url=AMADEUS_FLIGHT_OFFERS_ENDPOINT, 
            headers=headers, 
            params=query
            )
        all_fliights = response.json()

        with open(f'{destination_city_code}-flights.json', 'w') as file:
            json.dump(all_fliights, file, indent=4)
            print("json file created")

        return all_fliights