import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


# environment variables for "Nutritionix" (public)
HOST_DOMAIN = 'https://trackapi.nutritionix.com'
ENDPOINT = '/v2/natural/exercise'

def nutritionix_post_request(sentance, app_id, app_key):
    """
    function recives a sentance, sends a POST request and returns 
    the final parameters  
    """
    # url by endpoint
    url = HOST_DOMAIN + ENDPOINT

    # requests headers
    headers = {
        'Content-Type': 'application/json',
        "x-app-id": app_id,
        "x-app-key": app_key,
        "x-remote-user-id": "0"
        }

    # requests payload in a dictionary format
    payload = {
        "query": sentance
    }
    
    # POST request and response
    response = requests.post(url=url, headers=headers, json=payload)
    data = response.json()
    
    # retrieving important variables
    exercise = data["exercises"][0]["name"]
    duration = data["exercises"][0]["duration_min"]
    calories = data["exercises"][0]["nf_calories"]

    return exercise, duration, calories

def time_and_date():
    """
    function finds current date and time
    """
    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")
    return today_date, now_time

def new_sheet_row(date, time, exercise, duration, calories, workout_sheet_endpoint, sheet_bearer_token):
    """
    function recives all row parameters and 
    makes a POST request to update the google sheet
    """
    # requests headers
    headers = {
        'Authorization': f'Bearer {sheet_bearer_token}',
        'Content-Type': 'application/json'
    }

    # preparing the row content for the request body
    row_content = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }

    requests.post(url=workout_sheet_endpoint, json=row_content, headers=headers)
    print(f"row was added sucessfully")

def main():
    """ main function """

    # variables to access sheet (private)
    app_id = os.getenv("APP_ID")
    app_key = os.getenv("APP_KEY")
    workout_sheet_endpoint = os.getenv("WORKOUT_SHEET_ENDPOINT")
    sheet_bearer_token = os.getenv("SHEETY_BEARER_TOKEN")
    
    in_loop = True
    while in_loop:
        # ask for the exercise
        sentance = input("tell me about your exercise: ")

        # first function: find relevan variables from the sentance
        exercise, duration, calories = nutritionix_post_request(sentance=sentance, app_id=app_id, app_key=app_key)

        # second function: finds date and time
        date, time = time_and_date()

        # third function: makes a POST request to add a new row inside the goggle sheet
        new_sheet_row(date=date, time=time, exercise=exercise, duration=duration, calories=calories, workout_sheet_endpoint=workout_sheet_endpoint, sheet_bearer_token=sheet_bearer_token)

        
if __name__ == "__main__":
    main()
