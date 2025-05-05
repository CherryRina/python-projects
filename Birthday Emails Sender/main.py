"""
this program reads birthday information from CSV and sends a random letter out of 3 templates
with the name of the birthday person to his email
"""

# if you want to run successfully - edit the birthdays CSV (add todays date)
import os
import datetime as dt
from dotenv import load_dotenv
import pandas
import random
import smtplib

# permanent variables
load_dotenv()
my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")

# set todays date
now = dt.datetime.now()
now_month = now.month
now_day = now.day

# extract todays birthdays from CSV 
birthdays_data = pandas.read_csv("./birthdays.csv")                                             # reads csv to pandas DataFrame
this_months_birthdays = birthdays_data[birthdays_data.month == now_month]                       # all this months birthdays
todays_birthdays_dict = this_months_birthdays[this_months_birthdays.day == now_day].to_numpy()  # todays birthdays

# if there are birthdays today
if todays_birthdays_dict is not None:

    # send a random birthday message with their name
    for person_info in todays_birthdays_dict:
        
        # find credentials of the birthday person
        birthday_name = str(person_info[0])
        birthday_email = str(person_info[1])
        
        # choose random letter and read it
        chosen_letter_template = random.choice(["letter_1.txt", "letter_2.txt", "letter_3.txt"])
        path_to_letter = f"./letter_templates/{chosen_letter_template}"
        with open(path_to_letter, "r") as file:
            letter_template = "".join(file.readlines())

        # create new message
        message = letter_template.replace("[NAME]", birthday_name)

        #send an email to that person
        with smtplib.SMTP("smtp.gmail.com") as connection:          # creating a connection by mail provider
            connection.starttls()                                   # securing sent messages with TLS
            connection.login(user=my_email, password=password)    # connecting to my email account
            connection.sendmail(                                    # src, dst and content of the email
                from_addr=my_email,
                to_addrs=birthday_email,
                msg=message
            ) 