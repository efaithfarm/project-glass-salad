import unittest
import datetime as dt
from sensor_output_collector import check_data_freshness, summarize_freshness, format_freshness_report

class TestSensorCollector(unittest.TestCase):
    def test_newest_reading_wins(self):
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"2026-10-11 05:38:16"
            },
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"2026-10-12 05:38:16"
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["timestamp"],"2026-10-12 05:38:16")
        
    def test_older_reading_does_not_replace_newer(self):
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"2026-10-12 05:38:16"
            },
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"2026-10-11 05:38:16"
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["timestamp"],"2026-10-12 05:38:16")
    
    def test_empty_readings_returns_empty_list(self):
        result = check_data_freshness([])
        self.assertEqual(result,[])
        
    def test_invalid_timestamp_is_skipped(self):
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"2026-10-12 05:38:16"
            },
            {
                "SensorName":"G_A_sensor_A-3-2",
                "Timestamp":"The Sontaran Tenth Battle Fleet is unconcerned with timestamp accuracy!"
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["sensor_name"],"G_A_sensor_A-3-1")
        
    def test_invalid_timestamp_on_same_sensor_is_skipped(self):
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"2026-10-12 05:38:16"
            },
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"The Sontaran Tenth Battle Fleet is unconcerned with timestamp accuracy!"
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["sensor_name"],"G_A_sensor_A-3-1")
        self.assertEqual(result[0]["timestamp"],"2026-10-12 05:38:16")
        
    def test_missing_timestamp_is_skipped(self):
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":"2026-10-12 05:38:16"
            },
            {
                "SensorName":"G_A_sensor_A-3-2"
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["sensor_name"],"G_A_sensor_A-3-1")
        
    def test_missing_sensorname_is_skipped(self):
        readings = [
            {
                "Timestamp":"2026-10-12 05:38:16"
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(len(result),0)
        
    def test_empty_sensorname_is_skipped(self):
        readings = [
            {
                "SensorName":"",
                "Timestamp":"2026-10-12 05:38:16"
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(len(result),0)
        
    def test_non_dict_reading_is_skipped(self):
        readings = ["Stormageddon, Dark Lord of All"]
        result = check_data_freshness(readings)
        self.assertEqual(result, [])
        
    def test_old_reading_is_stale(self):
        old_timestamp = dt.datetime.now() - dt.timedelta(hours=2)
        old_timestamp = old_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":old_timestamp
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(result[0]["freshness_status"], "stale")
        
    def test_recent_reading_is_fresh(self):
        recent_timestamp = dt.datetime.now() - dt.timedelta(minutes=5)
        recent_timestamp = recent_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":recent_timestamp
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(result[0]["freshness_status"], "fresh")
        
    def test_future_reading_is_flagged(self):
        future_timestamp = dt.datetime.now() + dt.timedelta(hours=2)
        future_timestamp = future_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":future_timestamp
            }
        ]
        result = check_data_freshness(readings)
        self.assertEqual(result[0]["freshness_status"], "future")
        
    def test_exactly_one_hour_old_is_fresh(self):
        reference_time = dt.datetime(2026,10,21,12,0,0)
        reading_time = reference_time - dt.timedelta(hours=1)
        reading_time = reading_time.strftime('%Y-%m-%d %H:%M:%S')
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":reading_time
            }
        ]
        result = check_data_freshness(readings, reference_time=reference_time)
        self.assertEqual(result[0]["freshness_status"], "fresh")
        
        
    def test_one_second_past_fresh_is_stale(self):
        reference_time = dt.datetime(2026,10,21,12,0,0)
        reading_time = reference_time - dt.timedelta(hours=1, seconds=1)
        reading_time = reading_time.strftime('%Y-%m-%d %H:%M:%S')
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":reading_time
            }
        ]
        result = check_data_freshness(readings, reference_time=reference_time)
        self.assertEqual(result[0]["freshness_status"], "stale")
        
    def test_result_contains_expected_fields(self):
        reference_time = dt.datetime(2026,10,21,12,0,0)
        reading_time = reference_time - dt.timedelta(hours=1)
        reading_time = reading_time.strftime('%Y-%m-%d %H:%M:%S')
        readings = [
            {
                "SensorName":"G_A_sensor_A-3-1",
                "Timestamp":reading_time
            }
        ]
        result = check_data_freshness(readings, reference_time=reference_time)
        self.assertIn("sensor_name", result[0])
        self.assertIn("timestamp", result[0])
        self.assertIn("freshness_status", result[0])
        
    def test_summarize_freshness_counts_statuses(self):
        readings = [
            {
                "freshness_status":"fresh"
            },
            {
                "freshness_status":"fresh"
            },
            {
                "freshness_status":"stale"
            },
            {
                "freshness_status":"future"
            }
        ]
        expected_result = {
            "total":4,
            "fresh":2,
            "stale":1,
            "future":1
        }
        result = summarize_freshness(readings)
        self.assertEqual(result, expected_result)
        
    def test_summarize_empty_list(self):
        readings = []
        expected_result = {
            "total":0,
            "fresh":0,
            "stale":0,
            "future":0
        }
        result = summarize_freshness(readings)
        self.assertEqual(result, expected_result)
        
    def test_format_freshness_reporting(self):
        readings = {
            "total":4,
            "fresh":2,
            "stale":1,
            "future":1
        }
        expected_result = (
            "SeedWatch Sensor Report\n"
            "-----------------------\n"
            "Sensors checked: 4\n"
            "Fresh: 2\n"
            "Stale: 1\n"
            "Future: 1"
        )
        result = format_freshness_report(readings)
        self.assertEqual(result, expected_result)