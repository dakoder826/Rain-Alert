import requests
import os
from twilio.rest import Client

# Initializing variable to store api endpoint url
Endpoint_URL = "https://api.openweathermap.org/data/2.8/onecall"
# Variable for API key
api_key = os.getenv("API_KEY")
print(api_key)
# Variables for sending SMS
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

lat = os.getenv("MY_LAT")
lon = os.getenv("MY_LONG")
print(lat)
# Parameters for endpoints
parameters = {
    "lat": float(lat),
    "lon": float(lon),
    "appid": api_key,
    "exclude": "current, minutely, daily"

}

# Getting data from endpoint and saving it in json format in weather_data variable
response = requests.get(url=Endpoint_URL, params=parameters)
response.raise_for_status()
weather_data = response.json()

# Getting weather data for first twelve hours from the weather_data dicitonary
weather_slice = weather_data["hourly"][:12]
# Initializing variable to check if it will rain
will_rain = False


# Looping through sliced data to check if it will rain, if it does, set will_rain boolean to true
for hour_data in weather_slice:
    # Getting weather for each hour; weather id indicates the type of weather
    condition_code = hour_data["weather"][0]["id"]
    # If weather id less than 600, it means it will rain
    if int(condition_code) < 600:
        print(hour_data["weather"][0])
        will_rain = True
will_rain = True

# If will_rain boolean is set to true, send message to my phone
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Bring an umbrella",
        from_=os.getenv("TWILIO_NUMBER"),
        to=os.getenv("PHONE_NUMBER")
    )
print(message.status)

