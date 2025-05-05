""" 
every 60 seconds, this program will check if the ISS is near Ramat-Gan during night time
if it is - this program will send an email to "look up at the sky"
"""
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import smtplib
import time

# global params - loccation
my_lat = 20
my_lng = 20

# global params - email
password = os.getenv("PASSWORD")
my_email = os.getenv("MY_EMAIL")
dest_email = os.getenv("DEST_EMAIL")

# programs functions
def iss_is_near():
    ''' function searces for iss position and returns True if th iss is near me '''
    # catch iss api get response 
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    # finding iss location by api response
    iss_data = iss_response.json()
    latitude = float(iss_data["iss_position"]["latitude"])
    longitude = float(iss_data["iss_position"]["longitude"])
    print(f"DEBUG: iss location: {latitude} - {longitude}")

    # if the iss is near returns True
    if my_lat-5 <= latitude <= my_lat+5 and my_lng-5 <= longitude <= my_lng+5:
        return True
    else:
        return False
    
def is_night_time():
    ''' function finds sunset an rise time and returns True if its nightime '''
    # parameters for sun api get request
    parameters = {
        "lat": my_lat,
        "lng": my_lng,
        "formatted": 0,
        "tzid": "Asia/Tel_Aviv"
    }

    # catch sun api get response 
    sun_response = requests.get(url=" https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()

    # extracting sunset and sunrise hours
    sun_data = sun_response.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    # find my current hour
    current_hour = datetime.now().hour

    print(f"DEBUG: sunset {sunset} sunrise {sunrise}")
    print(f"DEBUG: my time: {current_hour}")

    # if its nightime returns True
    if current_hour >= sunset or current_hour <= sunrise:
        return True
    else:
        return False

def write_email():
    """ function sends an email message """
    # email message creation
    message = "Subject:ISS notification\n\nlook at the nightsky, the ISS is passing by!"

     # smtp connection
    with smtplib.SMTP("smtp.gmail.com") as connection:          # creating a connection by mail provider
        connection.starttls()                                   # securing sent messages with TLS
        connection.login(user= my_email, password= password)    # connecting to the mail account
        connection.sendmail(                                    # src, dst and content of mail     
            from_addr=my_email,
            to_addrs=dest_email,
            msg=message
        ) 
    print("an email was sent")

def main():
    """ main function """
    # run every 60 seconds
    while True:

        # sleeps for 60 seconds
        time.sleep(60)

        # if the iss is near and it is night time - send an email
        if iss_is_near() and is_night_time():
            write_email()

if __name__ == "__main__":
    main()