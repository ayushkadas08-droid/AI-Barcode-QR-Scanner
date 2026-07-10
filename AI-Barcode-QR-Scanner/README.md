# AI Barcode and QR Code Scanner

An internship project that scans QR codes and barcodes from uploaded images or webcam input, then uses an agentic AI workflow to classify the content, analyze safety risks, recommend a next action, and generate a short explanation.

## Features

- Upload-image scanning for QR codes and barcodes
- Webcam scanning with screenshot capture and optional website opening
- Image preprocessing for clearer detection on low-contrast or small codes
- Local safety analysis for scanned links
- Scan-agent classification for URLs, Wi-Fi QR codes, email, phone/SMS, product barcodes, and plain text
- Gemini-powered explanation using the safety and agent decision as context
- Recent scan history stored locally with SQLite

## Tech Stack

- Python
- Flask
- OpenCV
- ZXing-C++
- SQLite
- Gemini API

## Setup

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Create a local `.env` file in the project folder:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Run the Flask app:

```bash
python app.py
```

4. Open the local Flask URL shown in the terminal.

## How It Works

1. The user uploads an image or opens the webcam scanner.
2. The scanner tries multiple image versions, including grayscale, contrast-enhanced, enlarged, and thresholded images.
3. Detected QR codes and barcodes are deduplicated.
4. The safety service checks obvious risk signals, such as non-HTTPS URLs, short links, IP-address links, suspicious words, and unusually long URLs.
5. The scan agent classifies the decoded content and recommends the next action.
6. Gemini generates a short explanation using both the local safety result and the scan-agent decision.
7. Completed scan results are saved in local history.

## Security Note

Do not commit your real Gemini API key. The `.env` file is ignored by Git, and `.env.example` shows the expected format without exposing the secret.

The project reads `.env` directly, so no extra dotenv package is required.

If an API key was ever committed or shared, revoke it and create a new one.

## Testing

Run the focused service tests:

```bash
python -m unittest
```
