from typing import List, Dict, Any


SEVERITY_POINTS = {
    "LOW": 10,
    "MEDIUM": 25,
    "HIGH": 40,
    "CRITICAL": 60
}


def calculate_score(findings: List[Dict[str, Any]]) -> int:
    score = 0

    for finding in findings:
        severity = finding.get("severity", "LOW")
        score += SEVERITY_POINTS.get(severity, 10)

    return min(score, 100)


def get_risk_level(score: int) -> str:
    if score >= 90:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"
