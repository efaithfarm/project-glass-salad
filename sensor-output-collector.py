###
### SeedWatch - a simulated greenhouse sensor system
### Scott Hamilton
### sensor-output-collector: fetches sensor data and feeds it to repository based on freshness
###

import datetime as dt
import json
from pathlib import Path
import requests
from pprint import pprint

freshness_threshold = dt.timedelta(hours=1)

json_file_loc = "http://localhost:8080/sample_sensor_data.json"

sensor_readings = []

def fetch_sensor_data(location):
    http_session = requests.session()
    try:
        sensor_response = http_session.request(method='GET',url=location,timeout=5)
    except requests.exceptions.ConnectionError:
        print("Connection failed. Is the fucking server running?")
        return ""
    except requests.exceptions.Timeout:
        print("Even the Girl Who Waited is done waiting for this crap.")
        return ""
    response_code = sensor_response.status_code
    print(response_code)
    if response_code == 200:
        try:
            sensor_data = sensor_response.json()    
        except requests.exceptions.JSONDecodeError:
            print("You are tiny. I can see the whole of time and space. Every single atom of your existence, and I divide them.")
            return ""
        return sensor_data
    elif response_code == 404:
        json_no_worky = "What is wrong with you? Why would we even have a file called that. NOT FOUND, DUMBASS."
        print(json_no_worky)
        return json_no_worky
    else:
        bad_response = "I don't even know where to start. What did you do this time?"
        print(bad_response)
        return bad_response

def check_data_freshness(sensor_output):
    extract_time = dt.datetime.now()
    freshness_data = []
    latest_readings = {}
    if not sensor_output:
        print("The Library is silent. And this list is empty. We have a Vashta Nerada problem.")
    for reading in sensor_output:
        if isinstance(reading,dict) is False:
            print("not a dict, not interested")
            continue
        sensor_name = reading.get("SensorName", "Unknown")
        timestamp = reading.get("Timestamp", "Unknown")
        if timestamp == "Unknown":
            print("This timestamp is unacceptable. Witness now the subjugation of Earth for the glory of Sontar.")
            continue
        try:
            timestamp_conv = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Sontarans have NO WEAKNESS. Well, except timestamp-related ValueErrors. Oh, and their probic vents.")
            continue
        if sensor_name in latest_readings:
            previous_timestamp = latest_readings[sensor_name].get("Timestamp", "Unknown")
            try:
                previous_timestamp_conv = dt.datetime.strptime(previous_timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("A ValueError here means you will be melted with acid. Er, not melted with acid. Old habits.")
            if previous_timestamp_conv < timestamp_conv:
                print("THERE CAN ONLY BE ONE. In this case, 'ONE' refers to the newer timestamp.")
                latest_readings[sensor_name] = reading
        else:
            latest_readings[sensor_name] = reading
    for item in latest_readings.values():
        sensor_name = item.get("SensorName", "Unknown")
        timestamp = item.get("Timestamp", "Unknown")
        try:
            timestamp_conv = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Strptime used ValueError! It's super effective! (at breaking the code)")
            continue
        freshness = "fresh"
        time_difference = extract_time - timestamp_conv
        if time_difference > freshness_threshold:
            freshness = "stale"
        elif time_difference < dt.timedelta(0):
            freshness = "future"
        sensor_data = {
            "sensor_name": sensor_name,
            "freshness_status": freshness,
            "timestamp": timestamp
        }
        freshness_data.append(sensor_data)
    return freshness_data
            
def read_sensor_data(sensor_data):
    for datum in sensor_data:
        if datum["freshness_status"] == "fresh":
            print(datum["sensor_name"] + " is up to date. Last reading at " + datum["timestamp"])
        elif datum["freshness_status"] == "stale":
            print(datum["sensor_name"] + " is experiencing data delays. Last reading at " + datum["timestamp"])
        elif datum["freshness_status"] == "future":
            print(datum["sensor_name"] + " is experiencing a temporal anomaly. Last reading at " + datum["timestamp"])
            
sensor_readings = fetch_sensor_data(json_file_loc)

if isinstance(sensor_readings,list):
    check_results = check_data_freshness(sensor_readings)
    read_sensor_data(check_results)
else:
    print("I would recommend reading the error messages above. They will tell you why your shit is all fucked.")
