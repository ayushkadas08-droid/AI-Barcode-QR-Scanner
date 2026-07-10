import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9\s().-]{7,}$")


def analyze_scan_intent(code_type, data, safety):
    text = (data or "").strip()
    category = _classify_content(code_type, text)
    action = _recommend_action(category, safety)

    return {
        "category": category,
        "action": action,
        "confidence": _estimate_confidence(category, text),
        "reason": _build_reason(category, safety),
    }


def _classify_content(code_type, text):
    lowered = text.lower()

    if lowered.startswith(("http://", "https://")):
        return "Website URL"

    if lowered.startswith("wifi:"):
        return "Wi-Fi Configuration"

    if lowered.startswith("mailto:") or EMAIL_PATTERN.match(text):
        return "Email Address"

    if code_type != "QR Code" and text.isdigit():
        return "Product Barcode"

    if lowered.startswith(("tel:", "sms:")) or PHONE_PATTERN.match(text):
        return "Phone or SMS"

    if text:
        return "Plain Text"

    return "Unknown"


def _recommend_action(category, safety):
    safety_level = safety.get("level", "Unknown") if safety else "Unknown"

    if safety_level == "High Risk":
        return "Do not open automatically. Ask the user to verify the source first."

    if safety_level == "Caution":
        return "Show a warning and let the user decide whether to continue."

    if category == "Website URL":
        return "Offer to open the link after showing the safety summary."

    if category == "Wi-Fi Configuration":
        return "Show the network details and ask before connecting."

    if category == "Email Address":
        return "Offer to compose an email after confirming the address."

    if category == "Phone or SMS":
        return "Offer call or message options after confirming the number."

    if category == "Product Barcode":
        return "Use the barcode number for product lookup or inventory search."

    return "Display the decoded content for the user to copy or review."


def _estimate_confidence(category, text):
    if category == "Unknown" or not text:
        return "Low"

    if category in {"Website URL", "Wi-Fi Configuration", "Email Address", "Product Barcode"}:
        return "High"

    return "Medium"


def _build_reason(category, safety):
    safety_level = safety.get("level", "Unknown") if safety else "Unknown"

    if category == "Website URL":
        return f"The decoded content is a link and the local safety level is {safety_level}."

    if category == "Product Barcode":
        return "The decoded content is numeric and came from a barcode format."

    return f"The decoded content pattern matches {category.lower()}."
