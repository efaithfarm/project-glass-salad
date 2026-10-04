###
### SeedWatch - a simulated greenhouse sensor system
### Scott Hamilton
### sensor-output-collector: fetches sensor data and feeds it to repository based on freshness
###

import datetime as dt
import json
from pathlib import Path
import requests

freshness_threshold = dt.timedelta(hours=1)

json_file_loc = "http://localhost:8080/sorry_man_no_can_do.json"

sensor_readings = []

def fetch_sensor_data(location):
    http_session = requests.session()
    sensor_response = http_session.request(method='GET',url=location)
    response_code = sensor_response.status_code
    print(response_code)
    if response_code == 200:
        sensor_data = sensor_response.json()    
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
    for reading in sensor_output:
        sensor_name = reading.get("SensorName", "Unknown")
        timestamp = reading.get("Timestamp", "Unknown")
        freshness = True
        timestamp_conv = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        time_difference = extract_time - timestamp_conv
        if time_difference > freshness_threshold:
            freshness = False
        sensor_data = {
            "sensor_name": sensor_name,
            "freshness": freshness,
            "timestamp": timestamp
        }
        freshness_data.append(sensor_data)
    return freshness_data
            
def read_sensor_data(sensor_data):
    for datum in sensor_data:
        if datum["freshness"]:
            print(datum["sensor_name"] + " is up to date. Last reading at " + datum["timestamp"])
        else:
            print(datum["sensor_name"] + " is experiencing data delays. Last reading at " + datum["timestamp"])
            
sensor_readings = fetch_sensor_data(json_file_loc)

if isinstance(sensor_readings,list):
    check_results = check_data_freshness(sensor_readings)
    read_sensor_data(check_results)
else:
    print("I would recommend reading the error messages above. They will tell you why your shit is all fucked.")
