import os
import requests
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    
    def __init__(self):
        self.endpoint = os.getenv("SHEETY_ENDPOINT")
        self.bearer = os.getenv("SHEETY_BAERER")
        self.destination_data = {}
        self.headers = {
            'Authorization': f"Bearer {self.bearer}"
        }

    def get_destination_data(self):
        """ function initiates a GET request and returns the responce as JSON """
        response = requests.get(url=self.endpoint, headers=self.headers)
        self.destination_data = response.json()["prices"]
        return self.destination_data
    
    def update_destination_codes(self):
        """ method updates the iata code in the sheet """
        for row in self.destination_data:
            body = {
                    "price": {
                        "iataCode": row["iataCode"],
                    }
                }
            response = requests.put(
                url=f"{self.endpoint}/{row["id"]}",
                headers=self.headers,
                json=body
                )
            print(f"row updated: {response.status_code}")