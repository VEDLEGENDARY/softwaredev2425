import threading
import asyncio
from flask import Flask, jsonify, request
import json
import requests
import sched, time as time_module
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime
from types import SimpleNamespace
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiohttp
import mysql.connector
from mysql.connector import Error
import time
import hashlib


# TODO
# Make sports email system 
# Make twilio work or find another alternative 

DB_PASSWORD = "0324"
DB_PORT = "3305"

app = Flask(__name__)
api_operable = True
reqHeadersZen = {"Content-Type":"application/json"}
HASH_FILE_PATH  = "server_storage/hashes.json"
LOGS_FILE_PATH = "server_storage/logs.txt"

now = datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
localTimeZone = local_tz.tzname(local_now)
log_date = now.strftime("%m/%d/%Y")
log_time = now.strftime("%I:%M %p")

@app.route('/')
def test():
    return "test"


############### DATABASE INTERACTION ###############



def formatDatabaseQuery(data, table_name, hash, type, dbconnection):
    # SANITIZE DATA FIRST!!!!!!!!!!!!!!!!

    if type == "hashSave":
        sysdata = data['systemData']

        query = """
        INSERT INTO %s VALUES (
        "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"
        );

        """ % (table_name, hash, sysdata['platform'], sysdata['platform-release'], sysdata['platform-version'], sysdata['architecture'], sysdata['processor'], sysdata['hostname'], sysdata['ram'])
        return query


    elif type == "verifyHash":
        query ="""
        SELECT hash FROM %s
        """ % (table_name)


        cursor = dbconnection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        # print(data)
        return data
    

async def execute_query(query, databaseConnection, session):
    async with session:
        cursor = databaseConnection.cursor()
        try:
            # cursor.execute('SET GLOBAL max_allowed_packet=67108864')
            cursor.execute(query)
            databaseConnection.commit()
            console_log(f"[{databaseConnection.database}]: DATA WRITTEN TO DATABASE")
            return True

        except Error as err:
            console_log(f"[{databaseConnection.database}] [DATABASE INSERTION ERROR]: {err}", error=2)
            return False
    


async def create_database_connection(databaseName, session):
    console_log(f"[{databaseName}]: CREATING SQL DATABASE CONNECTION")
    databaseConnection = None
    try:
        async with session:
            if databaseName == "verifiedclients":
                databaseConnection = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    passwd = DB_PASSWORD,
                    port = DB_PORT,
                    database = databaseName,
                    auth_plugin = "mysql_native_password"
                )

                console_log(f"[{databaseName}]: SQL DATABASE CONNECTION SUCCESSFUL")
                return databaseConnection

    except Error as err:
        if "2003" in str(err):
            console_log(f"[{databaseName}] [SQL DATABASE CONNECTION ERROR]: NO SQL DATABASE FOUND ON HOST MACHINE (error 2003)", error=2)
        else:
            console_log(f"[{databaseName}] [SQL DATABASE CONNECTION ERROR]: {err}", error=2)

        return 1


############### DATABASE INTERACTION ###############


def console_log(args, error=None):
    if error:
        if error == 1: # Static red
            print(f"\033[91m{log_time} | {args}\033[0m")
        elif error == 2: # Blinking red
            print(f"\033[91m\33[5m{log_time} | {args}\33[5m\033[0m")
        else:
            pass
    else:
        print(f"{log_time} | {args}")

    # with open(LOGS_FILE_PATH, "w") as f:
    #     f.writelines(f"{log_date} - {log_time} | {args}\n")



def send_data(body, subject, email, type, hash):
    for i in email:
            me = "noreply.informationassistant@gmail.com"
            you = i

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = me
            msg['To'] = you

            html = f"""\
                {body}
            """
            part1 = MIMEText(html, 'html')
            msg.attach(part1)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(me, "inewptafzoguzxhv")
                smtp.sendmail(me, you, msg.as_string())

            console_log(f"[{hash}]: {type} sent to {i} at {log_time}")

    

def waitTime(email, exec_time, body, subject, type, hash):
    console_log(f"{type} email to {email} cued for {exec_time}")
    scheduler = sched.scheduler(time_module.time, time_module.sleep)
    t = time_module.strptime(exec_time, '%m-%d-%Y %H:%M:%S')
    t = time_module.mktime(t)
    scheduler_e = scheduler.enterabs(t, 1, send_data, (body, subject, email, type, hash))
    scheduler.run()


async def handleDataWeather():

    async def parse_weather(apiWeatherdataCurrent, apiWeatherdataForecast):
        console_log(f"[{clientHash}]: PARSING WEATHER DATA...")
        # If any one attribute of the flags below is set to shown, the flag will be set to true as a 
        # new column will need to be created in the payload.

        ########################################### CURRENT ###########################################

        current_conditions = apiWeatherdataCurrent['current']
        
        global location
        location = f"{apiWeatherdataCurrent['location']['name']}, {apiWeatherdataCurrent['location']['region']}"
        last_updated = current_conditions['last_updated']
        temp_c = current_conditions['temp_c']
        temp_f = current_conditions['temp_f']
        condition = current_conditions['condition']['text']
        wind_mph = current_conditions['wind_mph']
        wind_kph = current_conditions['wind_kph']
        wind_degree = current_conditions['wind_degree']
        wind_dir = current_conditions['wind_dir']
        pressure_mb = current_conditions['pressure_mb']
        pressure_in = current_conditions['pressure_in']
        precip_mm = current_conditions['precip_mm']
        precip_in = current_conditions['precip_in']
        humidity = current_conditions['humidity']
        feelslike_c = current_conditions['feelslike_c']
        feelslike_f = current_conditions['feelslike_f']
        vis_km = current_conditions['vis_km']
        vis_miles = current_conditions['vis_miles']
        uv = current_conditions['uv']
        gust_mph = current_conditions['gust_mph']
        gust_kph = current_conditions['gust_kph']
            
        global weather_list
        weather_list = {"data":[]}
        
        weather_list['data'].append( {"location": location} )

        if conditionBool:
            weather_list['data'].append( {"current_conditions": condition} )
        else:
            pass

        if temperatureBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"current_temperature": f"{temp_f} F"} )
            elif unitSystem == "metric":
                weather_list['data'].append( {"current_temperature": f"{temp_c} C"} )
            else:
                # Display some kind of error
                pass
        else:
            pass

        if windspdBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"current_wind_speed": f"{wind_mph} MPH"} )
            elif unitSystem == "metric":
                weather_list['data'].append( {"current_wind_speed": f"{wind_kph} KPH"} )
            else:
                pass
        else:
            pass

        if windDirBool:
            weather_list['data'].append( {"current_wind_direction": f"{wind_degree} degrees ({wind_dir})"} )
            
        else:
            pass

        if pressureBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"current_pressure": f"{pressure_in} in"} )
            elif unitSystem == "metric":
                weather_list['data'].append( {"current_pressure": f"{pressure_mb} mb"} )
            else:
                pass
        else:
            pass

        if precipBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"current_precipitation": f"{precip_in} in" } )
            elif unitSystem == "metric":
                weather_list['data'].append( {"current_precipitation": f"{precip_mm} mm"} )
            else:
                pass
        else:
            pass

        if humidityBool:
            weather_list['data'].append( {"current_humidity": f"{humidity} RH"} )
        else:
            pass

        if feelslikeBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"feels_like_temperature": f"{feelslike_f} F" } )
            elif unitSystem == "metric":
                weather_list['data'].append( {"feels_like_temperature": f"{feelslike_c} C"} )
            else:
                pass
        else:
            pass

        if visibilityBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"current_visibility": f"{vis_miles} Miles"} )
            elif unitSystem == "metric":
                weather_list['data'].append( {"current_visibility": f"{vis_km} KM"} )
            else:
                pass
        else:
            pass

        if uvBool:
            weather_list['data'].append( {"current_UV_index": f"{uv} nm"} )
        else:
            pass
        
        if windGustsBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"current_wind_gusts": f"{gust_mph} MPH"} )
            elif unitSystem == "metric":
                weather_list['data'].append( {"current_wind_gusts": f"{gust_kph} KPH"} )


        ########################################### FORECAST ###########################################

        forecastConditions = apiWeatherdataForecast['forecast']

        forecastCurrentDay = forecastConditions['forecastday'][0]['day']
        # print(forecastCurrentDay)

        maxtemp_c = forecastCurrentDay['maxtemp_c']
        maxtemp_f = forecastCurrentDay['maxtemp_f']
        mintemp_c = forecastCurrentDay['mintemp_c']
        mintemp_f = forecastCurrentDay['mintemp_f']
        avgtemp_c = forecastCurrentDay['avgtemp_c']
        avgtemp_f = forecastCurrentDay['avgtemp_f']
        maxwind_mph = forecastCurrentDay['maxwind_mph']
        maxwind_kph = forecastCurrentDay['maxwind_kph']
        totalprecip_mm = forecastCurrentDay['totalprecip_mm']
        totalprecip_in = forecastCurrentDay['totalprecip_in']
        totalsnow_cm = forecastCurrentDay['totalsnow_cm']
        avgvis_km = forecastCurrentDay['avgvis_km']
        avgvis_miles = forecastCurrentDay['avgvis_miles']
        avghumidity = forecastCurrentDay['avghumidity']
        daily_will_it_rain = forecastCurrentDay['daily_will_it_rain']
        daily_chance_of_rain = forecastCurrentDay['daily_chance_of_rain']
        daily_will_it_snow = forecastCurrentDay['daily_will_it_snow']
        daily_chance_of_snow = forecastCurrentDay['daily_chance_of_snow']
        conditionforecast = forecastCurrentDay['condition']['text']

        

        # weather_list.update("\033Today's outlook\033\n\n")

        if conditionBool:
            weather_list['data'].append({"conditions": conditionforecast} )
        else:
            pass

        if temperatureBool:
            if unitSystem == "imperial":
                weather_list['data'].append({"high": f"{maxtemp_f}F", "low": f"{mintemp_f}F"} )

            elif unitSystem == "metric":
                weather_list['data'].append({"high": f"{maxtemp_c}C", "low": f"{mintemp_c}C"} )
            else:
                # Display some kind of error
                pass
        else:
            pass

        if windspdBool:
            if unitSystem == "imperial":
                weather_list['data'].append({"max_wind_Speed":f"{maxwind_mph} MPH" } )
            elif unitSystem == "metric":
                weather_list['data'].append({"max_wind_Speed":f"{maxwind_kph} KPH" } )
            else:
                pass
        else:
            pass

        if precipBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"chance_of_precip": f"{daily_chance_of_rain}%", "total_precip": f"{totalprecip_in} in", "chance_of_snow": f"{daily_chance_of_snow}%", "total_snow": f"{totalsnow_cm} cm" } )
            elif unitSystem == "metric":
                weather_list['data'].append( {"chance_of_precip": f"{daily_chance_of_rain}%", "total_precip": f"{totalprecip_mm} mm", "chance_of_snow": f"{daily_chance_of_snow}%", "total_snow": f"{totalsnow_cm} cm" } )
            else:
                pass
        else:
            pass
        
        if humidityBool:
            weather_list['data'].append( {"average_humidity": f"{avghumidity} RH" } )
        else:
            pass

        if visibilityBool:
            if unitSystem == "imperial":
                weather_list['data'].append( {"average_visibility": f"{vis_miles} Miles" }  )
            elif unitSystem == "metric":
                weather_list['data'].append( {"average_visibility": f"{vis_km} Kilometers" }  )
            else:
                pass
        else:
            pass

        console_log(f"[{clientHash}]: WEATHER DATA PARSED, RETURNING DATA...")

    async def get_weather(session):
        console_log(f"[{clientHash}]: GETTING WEATHER...")
        currentFlag = False
        forecastFlag = False
        try:
            async with session.get(f"http://api.weatherapi.com/v1/current.json?key=a4e61d32b654481593404707222312&q={city}&aqi=no") as response0:
                apiWeatherdataCurrent = await response0.json()
                console_log(f"[{clientHash}]: WEATHER DATA RETRIEVED [CURRENT]")
                currentFlag = True
        except:
            console_log(f"[{clientHash}]: WEATHER DATA RETRIEVED [CURRENT]", error=1)
            # currentFlag will still be False 
            pass
        
        try:
            async with session.get(f"http://api.weatherapi.com/v1/forecast.json?key=a4e61d32b654481593404707222312&q={city}&days=1&aqi=no&alerts=yes") as response1:
                apiWeatherdataForecast = await response1.json()
                console_log(f"[{clientHash}]: WEATHER DATA RETRIEVED [FORECAST]")
                forecastFlag = True
        except:
            console_log(f"[{clientHash}]: WEATHER DATA RETRIEVED [FORECAST]", error=1)
            pass

        if response0.status == 400:
            return "invalidLoc"
        elif currentFlag and forecastFlag:
            await parse_weather(apiWeatherdataCurrent, apiWeatherdataForecast)
            return "success"
        else:
            return False


    weather_clientdata_settings = clientData['data']
    city = weather_clientdata_settings['city']
    email = weather_clientdata_settings['email'] # Remember to verify email via another API
    exec_time = weather_clientdata_settings['timeExec']

    # Toggle option settings (True / False format) #
    temperatureBool = weather_clientdata_settings['showTemperature']
    windspdBool = weather_clientdata_settings['showWindspeed'] # Windspeed 
    conditionBool = weather_clientdata_settings['showCondition'] # Current weather conditions 
    windGustsBool = weather_clientdata_settings['showWindgusts'] # Windgusts
    windDirBool = weather_clientdata_settings['showWindDirection'] # When returning return wind heading and direction (ex: Wind 360 - North)
    precipBool = weather_clientdata_settings['showPrecip'] # Precipitation 
    feelslikeBool = weather_clientdata_settings['showFeelslikeTemp'] # Feelslike Temp
    visibilityBool = weather_clientdata_settings['showVisibility'] # Visibility 
    pressureBool = weather_clientdata_settings['showPressure'] # Pressure 
    uvBool = weather_clientdata_settings['showUVIndex'] # UV Index 
    humidityBool = weather_clientdata_settings['showHumidity'] # Humidity
    


    async with aiohttp.ClientSession() as session:
        success = await get_weather(session)
        # print(success)
        if success == "success":
            return success # Works
        elif success == "invalidLoc":
            return success # Returns invalid location
        else:
            return False



async def handleNews(region):
        

    def parse_news(apiNewsdata):
        console_log(f"[{clientHash}]: PARSING NEWS DATA...")
        # write code to select a 3 random stories from the payloads
        # Int depends on which story you select
        nums = []
        # articles = apiNewsdata['articles'][0]
        # print(len(articles))
        # print(articles)
        for i in range(3):
            # make the last number the length of the list of articles in the json payload
            num = random.randint(0, 14)
            nums.append(num)


        author1 = apiNewsdata['articles'][nums[0]]['author']
        title1 = apiNewsdata['articles'][nums[0]]['title']
        descrip1 = apiNewsdata['articles'][nums[0]]['description']
        url1 = apiNewsdata['articles'][nums[0]]['url']

        author2 = apiNewsdata['articles'][nums[1]]['author']
        title2 = apiNewsdata['articles'][nums[1]]['title']
        descrip2 = apiNewsdata['articles'][nums[1]]['description']
        url2 = apiNewsdata['articles'][nums[1]]['url']

        author3 = apiNewsdata['articles'][nums[2]]['author']
        title3 = apiNewsdata['articles'][nums[2]]['title']
        descrip3 = apiNewsdata['articles'][nums[2]]['description']
        url3 = apiNewsdata['articles'][nums[2]]['url']
        

        global news_return_dict
        news_return_dict = {"data":[]}
        news_return_dict['data'].append( {
                            "title1": title1,
                            "description1": descrip1,
                            "story_URL1": url1,   
                                 
                            "title2": title2,
                            "description2": descrip2,
                            "story_URL2": url2,
                                   
                            "title3": title3,
                            "description3": descrip3,
                            "story_URL3": url3
        })

        console_log(f"[{clientHash}]: NEWS DATA PARSED, RETURNING DATA")
        

    async def get_news(region, session):
        console_log(f"[{clientHash}]: GETTING NEWS")
        async with session.get(f"https://newsapi.org/v2/top-headlines?country={region}&apiKey=d1fe035fe8494498b5505023fcddd3e0") as response:
            apiNewsdata = await response.json()
            reqStatus = apiNewsdata['status']

        if reqStatus == "ok":
            console_log(f"[{clientHash}]: NEWS RETRIEVED")
            parse_news(apiNewsdata)
            return True
        else:
            console_log(f"[{clientHash}]: FAILED TO RETRIEVE NEWS", error=1)
            return False

    email = clientData['data']['email']
    exec_time = clientData['data']['timeExec']


    async with aiohttp.ClientSession() as session:
        if await get_news(region, session):
            return True
        else:
            return False


async def handleQotd():
    email = clientData['data']['email']
    exec_time = clientData['data']['timeExec']

    async def get_qotd(session):
        console_log(f"[{clientHash}]: GETTING QOTD...")
        async with session.get("https://zenquotes.io/api/quotes/", headers=reqHeadersZen, ssl=False) as response0:
            response = await response0.json()
            if response0.status == 200:
                quote = response[0]['q']
                author = response[0]['a']


                global qotd_return_dict
                qotd_return_dict = {"data": []}
                qotd_return_dict['data'].append( {
                            "quote":  quote,
                            "author": author
                } )

                return True
            else:
                return False
        

    async with aiohttp.ClientSession() as session:
        if await get_qotd(session):
            console_log(f"[{clientHash}]: QOTD DATA RETRIEVED, RETURNING DATA")
            return True
        else:
            console_log(f"[{clientHash}]: FAILED TO RETRIEVE QOTD DATA", error=1)
            return False
    

async def handleOnThisDay():
    email = clientData['data']['email']
    exec_time = clientData['data']['timeExec']
    month = str(now.strftime("%m"))
    day = str(now.strftime("%d"))

    async def getData(session):
        console_log(f"[{clientHash}]: GETTING OTD DATA...")
        async with session.get(f'https://today.zenquotes.io/api/{month}/{day})', headers=reqHeadersZen, ssl=False) as response:
            try:
                otdData = await response.json()
                event = otdData['data']['Events'][0]['text']
                wikiLink = otdData['data']['Events'][0]['links']['1']['1']
                subject = otdData['data']['Events'][0]['links']['1']['2']


                global otd_return_dict
                otd_return_dict = {"data": []}
                otd_return_dict['data'].append( {
                            "date":f"{month}/{day}",
                            "event": event,
                            "subject": subject,
                            "wiki_url": wikiLink
                } )

                console_log(f"[{clientHash}]: OTD DATA RETRIEVED, RETURNING DATA")
                return True

            except:
                console_log(f"[{clientHash}]: UNABLE TO RETRIEVE OTD DATA", error=1)
                return False


    async with aiohttp.ClientSession() as session:
        if await getData(session):
            return True
        else:
            return False


async def verify_hash(hash, clientVersion):
    # return true if valid

    # return True
    console_log(F'[HASH: {hash}] [VER: {clientVersion}]: VERIFYING CLIENT ')
    async with aiohttp.ClientSession() as SqlVerifyHashSession:
        databaseConnection = await create_database_connection(databaseName="verifiedclients", session=SqlVerifyHashSession)
        if databaseConnection != 1:
            if databaseConnection.is_connected():
                hashColumnData = formatDatabaseQuery(data=None, table_name="clientData", hash=None, type="verifyHash", dbconnection=databaseConnection)
                for row in hashColumnData:
                    # print(row)
                    if row[0] == hash:
                        console_log(f"[HASH: {hash}] [VER: {clientVersion}]: HASH VALID")
                        return True
                    
                # If no match is found, return False
                console_log(f"[HASH: {hash}] [VER: {clientVersion}]: HASH INVALID", error=2)
                return False
        else:
            pass  # Error already raised

 

@app.route('/configData', methods=["POST"])
async def sort():
    console_log(f"[{request.remote_addr}]: INCOMING REQUEST")
    global clientData, clientHash
    clientData = request.get_json()
    dataType = clientData['dataType']
    clientHash = clientData['client_info']['hash']
    clientVer = clientData['client_info']['version']
    if await verify_hash(clientHash, clientVersion=clientVer):
        pass

    else:
        console_log(f"[HASH: {clientHash}] [VER: {clientVer}]: REJECTING REQUEST", error=2)
        return jsonify ( {"code": 2, "error": "Client hash invalid", "requested_hash": clientHash} )

    if dataType == "weather":
        console_log(f"[{clientHash}]: NEW WEATHER CONFIG DATA")
        global unitSystem
        allowed_units = {'imperial', 'metric'}
        unitSystem = clientData['data']['unitSystem']
        city = clientData['data']['city']
        if unitSystem in allowed_units:
            pass
        else:
            return jsonify ( {"code": 1, "error": f"The unit system '{unitSystem}' is not recognized"} ) 

        success = await handleDataWeather()
        if success == "success":
            console_log(f"[{clientHash}]: WEATHER DATA RETURNED")
            return jsonify ( {"code": 0, "return": weather_list})
        elif success == "invalidLoc":
            return jsonify ( {"code": 1, "error": f"The location '{city}' was not found"} )
        else:
            return jsonify ( {"code": 1, "error": "Server side error handling request"} )

    elif dataType == "news":
        region = clientData['data']['region']
        console_log(f"[{clientHash}]: INCOMING NEWS CONFIG DATA - REGION: '{region}'")
        if await handleNews(region):
            console_log(f"[{clientHash}]: NEWS DATA RETURNED")
            return jsonify ( {"code": 0, "return": news_return_dict} )
        else:
            return jsonify ( {"code": 1, "error": "Error retrieving API data"} )

    elif dataType == "qotd":
        console_log(f"[{clientHash}]: INCOMING QOTD CONFIG DATA")
        if await handleQotd():
            console_log(f"[{clientHash}]: QOTD DATA RETURNED")
            return jsonify ( {"code": 0, "return": qotd_return_dict} )
        else:
            return jsonify ( {"code": 1, "error": "Server side error handling request"} )

    elif dataType == "onThisDay":
        console_log(f"[{clientHash}]: INCOMING OTD CONFIG DATA")
        if await handleOnThisDay():
            console_log(f"[{clientHash}]: OTD DATA RETURNED")
            return jsonify ( {"code": 0, "return": otd_return_dict} )
        else:
            return jsonify ( {"code": 1, "error": "Server side error handling request"} )
    else:
        return jsonify ( {"code": 1, "error": f"Requested datatype '{dataType}' is invalid."} )



@app.route('/submitHtml', methods=['POST'])
async def r():
    data = request.get_json()
    hash = data['client_info']['hash']
    ver = data['client_info']['version']
    dataType = data['dataType']
    email = data['data']['email']
    exec_time = data['data']['timeExec']
    htmlData = data['data']['htmlData']
    subject = data['data']['subject']
    
    console_log(f"[{hash}]: RECEIVED EMAIL REQUEST")

    if await verify_hash(hash, clientVersion=ver):
        console_log(f"[{hash}]: {dataType} EMAIL REQUESTED - SENDING")
        threading.Thread(waitTime(email, exec_time, body=htmlData, subject=subject, type=dataType, hash=hash)).start()
        return jsonify({"code": 0})

    else:
        console_log(f"[HASH: {hash}] [VER: {ver}]: REJECTING REQUEST", error=2)
        return jsonify ( {"code": 2, "error": "Client hash invalid", "requested_hash": clientHash} )



    threading.Thread(waitTime(email, exec_time, body=htmlData, subject=subject, type=dataType, hash=hash)).start()
    return jsonify({"code": 0})


# Responds to the API callback requests 
@app.route('/apiStatus', methods=['GET'])
def reply():
    if api_operable:
        code = 0
    else:
        code = 1
    return jsonify( {"code": code} )


def generate_hash(mac_address):
    mac_bytes = mac_address.encode('utf-8')
    # Generate a SHA-256 hash from the MAC address bytes
    hash_object = hashlib.sha256(mac_bytes)
    hash_value = hash_object.hexdigest()
    # print(hash_value)
    return hash_value

async def logClient(Newhash, data):
    console_log(f"[{request.remote_addr}]: SAVING NEW HASH TO DATABASE - \033[34m[{Newhash}]\033[0m")
    parsed_data_querey = formatDatabaseQuery(data, table_name="clientData", hash=Newhash, type="hashSave", dbconnection=None)
    async with aiohttp.ClientSession() as Sqlsession:
            databaseConnection = await create_database_connection(databaseName="verifiedclients", session=Sqlsession)
            if databaseConnection != 1:
                if databaseConnection.is_connected():
                    dbConnectionID = databaseConnection.connection_id
                    if await execute_query(query=parsed_data_querey, databaseConnection=databaseConnection, session=Sqlsession):
                        try:
                            databaseConnection.close()
                            console_log(f"DATABASE CONNECTION SUCCESSFULLY CLOSED [CONNECTION ID: {dbConnectionID}]")
                        except:
                            console_log(f"[DATABASE ERROR]: UNABLE TO FORCEFULLY CLOSE DATABASE CONNECTION [Connection ID: {dbConnectionID}]", error=2)
                    else:
                        pass # Error already raised
                else:
                    # Make a retry counter
                    console_log("[DATABASE ERROR]: QUERY ATTEMPTED TO EXECUTE WHILE THERE WAS NO OPEN CONNECTION, RETRYING...", error=2)
                    time.sleep(2)
                    await logClient(Newhash, data)

            else:
                pass # Error already raised



@app.route("/getNewHash", methods=['POST'])
async def repl():
    console_log(f"[{request.remote_addr}]: ISSUING NEW HASH...")
    data = request.get_json()
    mac_addrs = data['systemData']['mac-address']
    Newhash = generate_hash(mac_addrs)
    await logClient(Newhash, data)
    console_log(f"[{request.remote_addr}]: NEW HASH RETURNED - \033[34m[{Newhash}]\033[0m")
    return jsonify ( {"newHash": Newhash} )


@app.route("/verifyHash", methods=["POST"])
async def rep():
    x = request.get_json()
    hash = x['hash']
    clientVer = x['clientVer']
    if await verify_hash(hash, clientVersion=clientVer):
        return jsonify( {"hashValid": True} )
    else:
        return jsonify( {"hashValid": False} )



# Runs the program and serves the API 
if __name__ == "__main__":
    appTask = asyncio.create_task(app.run(debug=True, host="0.0.0.0"))

