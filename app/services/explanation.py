from typing import List, Dict, Any


def build_summary(filename: str, findings: List[Dict[str, Any]], risk_level: str) -> str:
    if not findings:
        return (
            f"No major security issues were detected in {filename}. "
            "This does not guarantee the code is fully secure, but no MVP rules were triggered."
        )

    categories = sorted(set(item["category"] for item in findings))

    return (
        f"{filename} was reviewed by DevGuard AI. "
        f"The scan found {len(findings)} issue(s) across: {', '.join(categories)}. "
        f"Overall risk level is {risk_level}. "
        f"Review the recommendations before committing this code to GitHub or deploying it."
    )
