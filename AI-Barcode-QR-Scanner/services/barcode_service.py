import cv2
import zxingcpp


def scan_barcode(image):
    results = []

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    codes = zxingcpp.read_barcodes(image)

    for code in codes:

        if code.valid and "QR" not in str(code.format):

            results.append({
                "type": str(code.format),
                "data": code.text
            })

    return results
