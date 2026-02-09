import pdfplumber
import re

MANDATORY_FIELDS = [
    "policy_number",
    "policyholder_name",
    "date_of_loss",
    "location",
    "description",
    "claim_type",
    "estimated_damage"
]

def extract_fields(pdf_path: str):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    def find_inline(label):
        """
        Matches: LABEL: value (on the same line)
        """
        pattern = rf"{label}\s*:\s*(.+)"
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    fields = {}

    fields["policy_number"] = find_inline("POLICY NUMBER")
    fields["policyholder_name"] = find_inline("NAME OF INSURED")
    fields["date_of_loss"] = find_inline("DATE OF LOSS")
    fields["location"] = find_inline("LOCATION OF LOSS")

    # Description may span multiple words but is still same line in sample PDF
    fields["description"] = find_inline("DESCRIPTION OF ACCIDENT")

    fields["estimated_damage"] = find_inline("ESTIMATE AMOUNT")

    fields["claim_type"] = "injury" if "injur" in text.lower() else "vehicle"

    missing = [f for f in MANDATORY_FIELDS if not fields.get(f)]

    return fields, missing
