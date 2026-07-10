import cv2

from services.qr_service import scan_qr
from services.barcode_service import scan_barcode


def scan_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("The uploaded file could not be read as an image.")

    results = []

    for variant in _build_image_variants(image):
        results.extend(scan_qr(variant))
        results.extend(scan_barcode(variant))

    return _deduplicate_results(results)


def _build_image_variants(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)

    enlarged = cv2.resize(
        equalized,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    blurred = cv2.GaussianBlur(enlarged, (3, 3), 0)

    _, threshold = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return [
        image,
        gray,
        equalized,
        enlarged,
        threshold,
    ]


def _deduplicate_results(results):
    unique_results = []
    seen = set()

    for result in results:
        key = (result.get("type"), result.get("data"))

        if key in seen:
            continue

        seen.add(key)
        unique_results.append(result)

    return unique_results
