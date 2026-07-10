import google.generativeai as genai
from config import GEMINI_API_KEY

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Add it to a local .env file.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def explain_code(code_type, data, safety=None, agent=None):
    safety_text = "No local safety analysis was available."
    agent_text = "No scan-agent decision was available."

    if safety:
        warnings = safety.get("warnings") or []
        warning_text = "; ".join(warnings) if warnings else "No obvious warning signs."
        safety_text = f"""
        Local safety level: {safety.get("level")}
        Safety score: {safety.get("score")}/100
        Local summary: {safety.get("summary")}
        Warning signs: {warning_text}
        """

    if agent:
        agent_text = f"""
        Category: {agent.get("category")}
        Recommended action: {agent.get("action")}
        Confidence: {agent.get("confidence")}
        Reason: {agent.get("reason")}
        """

    prompt = f"""
    A user scanned a {code_type}.

    Decoded content:
    {data}

    Local safety analysis:
    {safety_text}

    Scan-agent decision:
    {agent_text}

    Explain:
    1. What this code contains.
    2. What the scan agent recommends.
    3. Whether it looks safe based on the local safety analysis.
    4. What the user should do next.
    Keep the answer under 120 words.
    """

    response = model.generate_content(prompt)

    return response.text
