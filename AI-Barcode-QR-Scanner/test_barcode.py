import unittest
from importlib.util import find_spec


@unittest.skipIf(find_spec("cv2") is None, "OpenCV is not installed in this Python environment.")
class BarcodeServiceTest(unittest.TestCase):
    def test_scan_barcode_function_is_available(self):
        from services.barcode_service import scan_barcode

        self.assertTrue(callable(scan_barcode))


if __name__ == "__main__":
    unittest.main()
