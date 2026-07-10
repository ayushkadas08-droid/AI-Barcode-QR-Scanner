from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = {
    "verify",
    "login",
    "password",
    "reset",
    "bank",
    "wallet",
    "free",
    "prize",
    "gift",
    "urgent",
    "account",
}

SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "shorturl.at",
}


def analyze_code_safety(data):
    text = (data or "").strip()
    lowered = text.lower()
    warnings = []

    if not text:
        return {
            "level": "Unknown",
            "score": 0,
            "summary": "No decoded content was available for safety analysis.",
            "warnings": ["Empty scan result"],
        }

    if not lowered.startswith(("http://", "https://")):
        return {
            "level": "Info",
            "score": 20,
            "summary": "This does not appear to be a website link.",
            "warnings": [],
        }

    parsed = urlparse(text)
    domain = parsed.netloc.lower()

    if lowered.startswith("http://"):
        warnings.append("The link does not use HTTPS.")

    if domain in SHORTENER_DOMAINS:
        warnings.append("The link uses a URL shortener, so the real destination is hidden.")

    if _looks_like_ip_address(domain):
        warnings.append("The link points directly to an IP address instead of a normal domain.")

    if "@" in text:
        warnings.append("The link contains '@', which can hide the real destination.")

    if any(keyword in lowered for keyword in SUSPICIOUS_KEYWORDS):
        warnings.append("The link contains words often used in phishing or scam pages.")

    if len(text) > 120:
        warnings.append("The link is unusually long and should be checked carefully.")

    if len(warnings) >= 3:
        level = "High Risk"
        score = 85
        summary = "This link has multiple warning signs. Do not open it unless you trust the source."
    elif warnings:
        level = "Caution"
        score = 55
        summary = "This link has one or more warning signs. Review it before opening."
    else:
        level = "Looks Safe"
        score = 15
        summary = "No obvious local warning signs were found, but only open it if you trust the source."

    return {
        "level": level,
        "score": score,
        "summary": summary,
        "warnings": warnings,
    }


def _looks_like_ip_address(domain):
    host = domain.split(":")[0]
    parts = host.split(".")

    if len(parts) != 4:
        return False

    return all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)
