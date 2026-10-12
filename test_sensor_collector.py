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