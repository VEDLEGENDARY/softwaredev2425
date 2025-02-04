import requests
import json
import datetime 
from datetime import datetime
import aiohttp
import asyncio
import time

# r = requests.get("http://api.weatherapi.com/v1/current.json?key=a4e61d32b654481593404707222312&q=Shreveport&aqi=no")
# print(r.text)

headers = {"Content-Type":"application/json"} 
baseUrl = "http://localhost:5000"
# baseUrl = "http://192.168.1.153:5000"

hash = "K81-1ed191e230cebacaaaa9c404ad40568de50f1fdf"
configdata = json.dumps( {
                        "client_info": {
                            "hash": hash,
                            "version": 1.0
                        },
                        "dataType": "weather",
                        "data": {
                            "city": "Dallas",
                            "unitSystem": 'imperial', 
                            "timeExec": '12-30-2022 21:45:00',
                            "email": ["f4andrew7@gmail.com"],
                            "showTemperature": True,
                            "showWindspeed": True,
                            "showWindgusts": True,
                            "showCondition": True, 
                            "showLastUpdatedTime": True, 
                            "showWindDirection": True,
                            "showPrecip": True, 
                            "showFeelslikeTemp": True,
                            "showVisibility": True, 
                            "showPressure": True,
                            "showUVIndex": True,
                            "showHumidity": True}} )

async def fetch(session, url):
    async with session.post(url, data=configdata, headers=headers) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        json_data = await fetch(session, baseUrl + "/configData")
        print(json.dumps(json_data, indent=4))  # Pretty-print the JSON data

start = time.time()
asyncio.run(main())
end = time.time()
print(f"[Async tasks]: {end - start} secs to complete\n")

# configdata = json.dumps( {  
#                         "client_info": {
#                             "hash": hash,
#                             "version": 1.0
#                             },
#                             "dataType": "news",
#                             "data": {
#                                 "region": "us", 
#                             "email": ["f4andrew7@gmail.com"], 
#                             "timeExec": '12-30-2022 21:45:00',

#                             }} )

# r = requests.post(baseUrl + "/configData", headers=headers, data=configdata)
# print(r.text)




#     city = clientData['']
#     unitSystem = clientData['']
#     email = clientData['']
#     phone = clientData['']

#     # Toggle option settings (True / False format)#
#     temptartureBool = clientData['']
#     windspdBool = clientData[''] # Windspeed 
#     condtionBool = clientData[''] # Current weather conditions 
#     lastUpdatedBool = clientData[''] # Time last updated 
#     windDirBool = clientData[''] # When returning return wind heading and direction (ex: Wind 360 - North)
#     precipBool = clientData[''] # Precipitation 
#     feelslikeBool = clientData[''] # Feelslike Temp
#     visibilityBool = clientData[''] # Visibility 
#     pressureBool = clientData[''] # Pressure 
#     uvBool = clientData[''] # UV Index 


# r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=d1fe035fe8494498b5505023fcddd3e0")
# print(r.text)
# now = datetime.now()
# local_now = now.astimezone()
# local_tz = local_now.tzinfo
# localTimeZone = local_tz.tzname(local_now)
# log_date = now.strftime("%m/%d/%Y")
# log_time = now.strftime("%I:%M %p")

# print(now.strftime("%m"))

# data = json.dumps ( {"dataType": "onThisDay", 
#                     "email": "f4andrew7@gmail.com",
#                     "timeExec": "12-30-2022 21:45:00"

# } )

# r = requests.post(baseUrl + "/configData", headers=headers, data=data)
# print(r.text)

# data = json.dumps({"new": 0})
# r = requests.post(baseUrl + "/getNewHash", headers=headers, data=data)
# print(r.text)