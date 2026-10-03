###
### SeedWatch - a simulated greenhouse sensor system
### Scott Hamilton
### sensor-output-collector: fetches sensor data and feeds it to repository based on freshness
###

#import requests
import datetime as dt

freshness_threshold = dt.timedelta(hours=1)

sensor_1_reading = {
    'SensorName':'G_A_sensor_A-3-1',
    'Location':'GreenhouseA_Row3_Box1',
    'Timestamp':'2026-10-03 06:37:42',
    'Metric':'Temperature',
    'Unit':'F',
    'Value':'77.3'
}
sensor_2_reading = {
    'SensorName':'G_A_sensor_A-3-2',
    'Location':'GreenhouseA_Row3_Box2',
    'Timestamp':'2026-10-03 06:38:16',
    'Metric':'Temperature',
    'Unit':'F',
    'Value':'77.7'
}
sensor_3_reading = {
    'SensorName':'G_A_sensor_A-3-3',
    'Location':'GreenhouseA_Row3_Box3',
    'Timestamp':'2026-10-03 05:37:49',
    'Metric':'Temperature',
    'Unit':'F',
    'Value':'77.2'
}

sensor_readings = [sensor_1_reading,sensor_2_reading,sensor_3_reading]

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
            
check_results = check_data_freshness(sensor_readings)

read_sensor_data(check_results)
#if __name__ == "__main__":