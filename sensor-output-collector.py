###
### SeedWatch - a simulated greenhouse sensor system
### Scott Hamilton
### sensor-output-collector: fetches sensor data and feeds it to repository based on freshness
###

#import requests
import datetime as dt
import json
from pathlib import Path

freshness_threshold = dt.timedelta(hours=1)

#print(__file__)

json_import_dir = (Path(__file__).parent)

json_file = json_import_dir / "sample_sensor_data.json"

sensor_readings = []

def fetch_sensor_data(json_path):
    #print(json_path)
    with open(json_path, 'r') as file:
        input_data = json.load(file)
    return input_data
    
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
            
sensor_readings = fetch_sensor_data(json_file)

check_results = check_data_freshness(sensor_readings)

read_sensor_data(check_results)
#if __name__ == "__main__":