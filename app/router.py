def route_claim(fields, missing):
    description = (fields.get("description") or "").lower()
    damage = int(fields.get("estimated_damage") or 0)

    if missing:
        return "Manual Review", "Mandatory fields missing"

    if any(word in description for word in ["fraud", "staged", "inconsistent"]):
        return "Investigation Flag", "Suspicious keywords detected"

    if fields.get("claim_type") == "injury":
        return "Specialist Queue", "Injury-related claim"

    if damage < 25000:
        return "Fast-track", "Low estimated damage"

    return "Manual Review", "Default routing"
