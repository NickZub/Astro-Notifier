import requests
import config
from datetime import date

#Fixed latitude and longitude for Newark.
URL = "https://www.7timer.info/bin/api.pl?"
params = {
    "lat": 40.7355,
    "lon": -74.1741,
    "product": 'astro',
    "unit": 'british',
    "output": 'json',
}

try:
    response = requests.get(URL, params).json()
except:
    quit()

#Uses the API scale from 1(Good)-8(Bad) to give weather descriptions.
def quality(x):
    if(x <= 2):
        return "Excellent"
    elif(x <= 4):
        return "Good"
    elif(x <= 6):
        return "Fair"
    else:
        return "Poor"

#Accessing the first few entries which relate to the current and next day over a period of 12 hours.
#The range and added values change depending on the hour the program runs because of the API.
#Add a value of 7 when done around 3:00, add a value of 1 when done around 6:00. Switch AM/PM.
message = ""
goodClouds = False
for data in response['dataseries'][:5]:
    time = data['timepoint'] + 1 % 12
    if(time < 12):
        message += f"{time} PM: "
    elif(time > 24):
        message += f"{time-24} PM: "
    else:
        message += f"{time-12} AM: "
    
    cloudCover = data['cloudcover']
    if(cloudCover <= 5):
        message += f"Up to {cloudCover}0% cloud coverage, "
        goodClouds = True
    else:
        message += f"Up to {cloudCover+1}0% cloud coverage, "

    message += f"{quality(data['transparency'])} transparency, {quality(data['seeing'])} seeing.\n\n"

#Pushover API Notifier. Only send a message under ideal conditions.
if(goodClouds):
    url = "https://api.pushover.net/1/messages.json"
    title = f"Forecast for {date.today().strftime('%m/%d/%y')}"
    pushoverRequest = {"token": config.APPLICATION_TOKEN,
                        "user": config.USER_TOKEN,
                        "title": title,
                        "message": message}
    requests.post(url, pushoverRequest)