import cv2
import zxingcpp
import os
import time
import webbrowser

# ------------------------------------
# Create capture folder
# ------------------------------------
os.makedirs("static/captures", exist_ok=True)

# ------------------------------------
# Webcam
# ------------------------------------
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

cv2.setUseOptimized(True)
cv2.setNumThreads(4)

if not cap.isOpened():
    print("Cannot open webcam.")
    exit()

font = cv2.FONT_HERSHEY_SIMPLEX

last_time = time.time()

current_url = None
last_opened_url = ""
last_open_time = 0
COOLDOWN = 5

print("--------------------------------------")
print("AI Barcode & QR Scanner")
print("--------------------------------------")
print("Q : Quit")
print("S : Save Screenshot")
print("O : Open Website")
print("--------------------------------------")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ------------------------------------
    # FPS
    # ------------------------------------
    current_time = time.time()
    fps = int(1 / (current_time - last_time + 0.0001))
    last_time = current_time

    current_url = None

    # ------------------------------------
    # Prepare multiple versions
    # ------------------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    equalized = cv2.equalizeHist(gray)

    enlarged = cv2.resize(
        equalized,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    _, thresh = cv2.threshold(
        enlarged,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    images = [
        frame,
        gray,
        equalized,
        enlarged,
        thresh
    ]

    detected = []

    # ------------------------------------
    # Try each image
    # ------------------------------------
    for img in images:

        codes = zxingcpp.read_barcodes(img)

        if codes:
            detected = codes
            break

    y = 35

    # ------------------------------------
    # Display Results
    # ------------------------------------
    for code in detected:

        if not code.valid:
            continue

        barcode_type = str(code.format)
        barcode_text = code.text

        print("Detected:", barcode_type)
        print("Text:", barcode_text)

        # -----------------------------
        # Draw bounding box
        # -----------------------------
        try:

            pos = code.position

            points = [
                (int(pos.top_left.x), int(pos.top_left.y)),
                (int(pos.top_right.x), int(pos.top_right.y)),
                (int(pos.bottom_right.x), int(pos.bottom_right.y)),
                (int(pos.bottom_left.x), int(pos.bottom_left.y))
            ]

            for i in range(4):
                cv2.line(
                    frame,
                    points[i],
                    points[(i + 1) % 4],
                    (0, 255, 0),
                    3
                )

        except:
            pass

        cv2.putText(
            frame,
            f"Type : {barcode_type}",
            (20, y),
            font,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            barcode_text,
            (20, y + 28),
            font,
            0.6,
            (255,255,255),
            2
        )

        y += 70

        if barcode_text.startswith(("http://", "https://")):
            current_url = barcode_text

    # ------------------------------------
    # Footer
    # ------------------------------------
    cv2.putText(
        frame,
        f"FPS : {fps}",
        (20, frame.shape[0]-70),
        font,
        0.6,
        (0,255,255),
        2
    )

    cv2.putText(
        frame,
        "S : Save",
        (20, frame.shape[0]-45),
        font,
        0.6,
        (255,255,255),
        2
    )

    cv2.putText(
        frame,
        "O : Open Website",
        (20, frame.shape[0]-20),
        font,
        0.6,
        (255,255,255),
        2
    )

    cv2.imshow("AI Barcode & QR Scanner", frame)

    # ------------------------------------
    # Keyboard
    # ------------------------------------
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    elif key == ord("s"):

        filename = f"static/captures/capture_{int(time.time())}.png"

        cv2.imwrite(filename, frame)

        print("Saved:", filename)

    elif key == ord("o"):

        if current_url:

            current = time.time()

            if (current_url != last_opened_url or
                current - last_open_time > COOLDOWN):

                webbrowser.open(current_url)

                last_opened_url = current_url
                last_open_time = current

# ------------------------------------
# Cleanup
# ------------------------------------
cap.release()
cv2.destroyAllWindows()