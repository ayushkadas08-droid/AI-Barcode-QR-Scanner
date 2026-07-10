# AI Barcode and QR Code Scanner

This is an internship project that scans QR codes and barcodes from uploaded images or webcam input. The system uses computer vision for detection and an agentic AI workflow to classify scanned content, analyze safety risks, recommend the next action, and generate a user-friendly explanation.

## Features

- Scan QR codes and barcodes from uploaded images
- Scan codes using the webcam
- Improve detection using image preprocessing
- Classify scanned content as URL, Wi-Fi QR, email, phone/SMS, product barcode, or plain text
- Analyze basic safety risks in scanned links
- Generate AI explanations using Gemini
- Recommend safe next actions for the user
- Store recent scan history locally using SQLite

## Agentic AI Workflow

The project follows an agent-like decision flow:

1. Decode the QR code or barcode.
2. Classify the decoded content.
3. Check for safety risks.
4. Decide the recommended user action.
5. Generate an AI explanation based on the scan result.

Example:

A scanned URL is checked for HTTPS, URL shorteners, suspicious keywords, and unusual patterns. The scan agent then recommends whether the user should open it, review it carefully, or avoid it.

## Tech Stack

- Python
- Flask
- OpenCV
- ZXing-C++
- SQLite
- Gemini API
- HTML/CSS

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/ayushkadas08-droid/AI-Barcode-QR-Scanner.git
cd AI-Barcode-QR-Scanner
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project folder:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the application:

```bash
python app.py
```

5. Open the Flask URL shown in the terminal.

Usually it is:

```text
http://127.0.0.1:5000
```

## Project Structure

```text
AI-Barcode-QR-Scanner/
|-- app.py
|-- scanner.py
|-- ai.py
|-- config.py
|-- requirements.txt
|-- README.md
|-- services/
|   |-- agent_service.py
|   |-- ai_service.py
|   |-- barcode_service.py
|   |-- history_service.py
|   |-- qr_service.py
|   `-- safety_service.py
|-- templates/
|   |-- index.html
|   |-- result.html
|   |-- history.html
|   `-- webcam.html
`-- static/
    `-- css/
        `-- style.css
```

## Security Note

The real Gemini API key should not be uploaded to GitHub.

Use `.env` for the real key:

```text
GEMINI_API_KEY=your_real_key_here
```

Use `.env.example` only as a safe template:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

The project reads `.env` directly, so no extra dotenv package is required.

If an API key was ever committed or shared, revoke it and create a new one.

## Testing

Run tests with:

```bash
python -m unittest
```

## Future Improvements

- Add product lookup for barcode numbers
- Add stronger phishing detection using external threat intelligence APIs
- Add user login and scan history per user
- Deploy the application online
- Add a mobile-friendly camera scanner
