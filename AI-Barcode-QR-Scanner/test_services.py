import unittest

from services.agent_service import analyze_scan_intent
from services.safety_service import analyze_code_safety


class SafetyServiceTest(unittest.TestCase):
    def test_safe_https_url_has_low_score(self):
        result = analyze_code_safety("https://google.com")

        self.assertEqual(result["level"], "Looks Safe")
        self.assertEqual(result["score"], 15)
        self.assertEqual(result["warnings"], [])

    def test_short_insecure_login_url_is_high_risk(self):
        result = analyze_code_safety("http://bit.ly/login-free-prize")

        self.assertEqual(result["level"], "High Risk")
        self.assertGreaterEqual(result["score"], 80)
        self.assertGreaterEqual(len(result["warnings"]), 3)


class AgentServiceTest(unittest.TestCase):
    def test_product_barcode_is_not_classified_as_phone(self):
        safety = analyze_code_safety("8901234567890")
        result = analyze_scan_intent("EAN-13", "8901234567890", safety)

        self.assertEqual(result["category"], "Product Barcode")
        self.assertEqual(result["confidence"], "High")

    def test_wifi_qr_is_classified(self):
        safety = analyze_code_safety("WIFI:T:WPA;S:CollegeWiFi;P:secret;;")
        result = analyze_scan_intent("QR Code", "WIFI:T:WPA;S:CollegeWiFi;P:secret;;", safety)

        self.assertEqual(result["category"], "Wi-Fi Configuration")


if __name__ == "__main__":
    unittest.main()
