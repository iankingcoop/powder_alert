import requests
import os
from twilio.rest import Client
from datetime import datetime


datetimez = []
formatted_timez = []

# weather API
api_key = os.environ["WEATHER_KEY"]
omw_endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# twilio API
account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(account_sid, auth_token)

# send_message "Snow on the way! Expected around: {DT}"
def send_message(datetimez):
    for i in datetimez:
        i = datetime.strptime(i, '%Y-%m-%d %H:%M:%S')
        i = i.strftime('%A, %H:%M:%S')
        formatted_timez.append(i)
        print(formatted_timez)
    message = client.messages.create(
        body=f"Snow on the way in the next 3 days! Expected snowfalls hours: \n\n{formatted_timez}",
        from_="+18556475303",
        to="+17036775244"
    )

    print(message.sid)


### locations ###
# CB
# weather_params = {
#     "lat": 38.9062842,
#     "lon": -106.9738503,
#     "appid": api_key,
# }

# Banks
# weather_params = {
#     "lat": 44.0804465,
#     "lon": -116.1327698,
#     "appid": api_key,
# }

# Heavenly
weather_params = {
    "lat": 38.9349226,
    "lon": -119.9402777,
    "appid": api_key,
}


response = requests.get(omw_endpoint, params=weather_params)
response.raise_for_status()
print(response)
print(response.status_code)
weather_data = response.json()
print(weather_data)

will_snow = False

# get data for next 3 days every day - there are eight three-hour data chunks in one day x3 for three days
for i in weather_data['list'][:23]:
    if 'snow' in i['weather'][0]['main'].lower():
        print('Snow on the way!')
        datetimez.append(weather_data['list'][weather_data['list'].index(i)]['dt_txt'])
        will_snow = True
        print(datetimez)


if will_snow == True:
    send_message(datetimez)
