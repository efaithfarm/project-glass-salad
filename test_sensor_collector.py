import unittest
from sensor_output_collector import check_data_freshness

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