import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("E:/EnvironmentVariables/.env.txt")

GENDER = "male"
WEIGHT_KG = 60
HEIGHT_CM = 182
AGE = 23
APP_ID = os.environ["APP_ID_NUTRITIONIX"]
API_KEY = os.environ["API_KEY_NUTRITIONIX"]
SHEETY_USERNAME = os.environ["SHEETY_USERNAME"]
SHEETY_PROJECT_NAME = "workoutTracking"
SHEETY_SHEET_NAME = "workouts"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/{SHEETY_PROJECT_NAME}/{SHEETY_SHEET_NAME}"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_desc = input("Please describe your exercise: ")

parameters = {
    "query": exercise_desc,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

today = datetime.now()

# inserting current date, time and results from Nutritionix API to variable named body that is
# dictionary (ultimately JSON) that matches the Sheety API requirements for inserting data into Google Sheet

for i in range(len(result['exercises'])):
    body = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": result["exercises"][i]['name'].title(),
            "duration": result["exercises"][i]['duration_min'],
            "calories": result["exercises"][i]['nf_calories']
        }
    }

    response_1 = requests.post(url=sheety_endpoint, json=body)
    print(response_1.text)
