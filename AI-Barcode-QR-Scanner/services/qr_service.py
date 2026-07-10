import cv2


def scan_qr(image):
    results = []
    detector = cv2.QRCodeDetector()

    multi_result = detector.detectAndDecodeMulti(image)

    if multi_result[0]:
        decoded_values = multi_result[1]

        for data in decoded_values:
            if data:
                results.append({
                    "type": "QR Code",
                    "data": data
                })

        return results

    data, _, _ = detector.detectAndDecode(image)

    if data:
        results.append({
            "type": "QR Code",
            "data": data
        })

    return results
