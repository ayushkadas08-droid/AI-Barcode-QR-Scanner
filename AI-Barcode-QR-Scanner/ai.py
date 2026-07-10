from services.ai_service import explain_code
from services.agent_service import analyze_scan_intent
from services.safety_service import analyze_code_safety


def explain_scan(results):
    """
    Adds an AI explanation to every detected code.
    """

    enhanced_results = []

    for result in results:
        safety = analyze_code_safety(result["data"])
        agent = analyze_scan_intent(result["type"], result["data"], safety)

        ai_text = explain_code(
            result["type"],
            result["data"],
            safety,
            agent
        )

        enhanced_results.append({
            "type": result["type"],
            "data": result["data"],
            "safety": safety,
            "agent": agent,
            "ai": ai_text
        })

    return enhanced_results
