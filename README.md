# FNOL Claims Routing – FastAPI Project

## Overview

This project implements an **Autonomous Insurance Claims Processing Agent** using **FastAPI**.

The system accepts FNOL (First Notice of Loss) PDF documents, extracts key claim fields, validates them, and **routes each claim to the correct workflow** via the `/process-claim` API endpoint.

---

## Key Features

* PDF upload via REST API
* FNOL field extraction from text-based PDFs
* Mandatory field validation
* Rule-based claim routing
* Explainable routing decision (reasoning)
* JSON response aligned with assessment requirements

---

## API Endpoint

### `POST /process-claim`

This is the **main routing endpoint**.

#### Request

* **Content-Type:** `multipart/form-data`
* **Body:**

  * `file`: FNOL PDF document

#### Example (Swagger UI)

```
http://127.0.0.1:8000/docs
```

Upload a PDF under `/process-claim`.

---

## Processing Flow

### 1. PDF Upload

The user uploads an FNOL PDF to `/process-claim`.

### 2. Field Extraction

The system extracts:

* Policy Number
* Policyholder Name
* Date of Loss
* Location of Loss
* Accident Description
* Estimated Damage
* Claim Type (injury / vehicle)

Extraction is performed in `extractor.py`.

---

### 3. Mandatory Field Validation

The following fields are mandatory:

* policy_number
* policyholder_name
* date_of_loss
* location
* description
* claim_type
* estimated_damage

If **any mandatory field is missing**, the claim is immediately routed to **Manual Review**.

---

## Routing Logic (`route_claim`)

The routing logic is implemented in `router.py` and applied after extraction.

### Routing Rules (in order)

```python
if missing:
    return "Manual Review", "Mandatory fields missing"

if any(word in description for word in ["fraud", "staged", "inconsistent"]):
    return "Investigation Flag", "Suspicious keywords detected"

if fields.get("claim_type") == "injury":
    return "Specialist Queue", "Injury-related claim"

if damage < 25000:
    return "Fast-track", "Low estimated damage"

return "Manual Review", "Default routing"
```

### Routing Outcomes

| Condition                | Route              |
| ------------------------ | ------------------ |
| Missing mandatory fields | Manual Review      |
| Fraud-related keywords   | Investigation Flag |
| Injury claim             | Specialist Queue   |
| Damage < 25,000          | Fast-track         |
| High-value, non-injury   | Manual Review      |

---

## Example Response

```json
{
  "extractedFields": {
    "policy_number": "POL123456789",
    "policyholder_name": "John Michael Doe",
    "date_of_loss": "12/04/2023",
    "location": "Near Empire State Building",
    "description": "Rear-end collision at a traffic signal",
    "estimated_damage": "26000",
    "claim_type": "injury"
  },
  "missingFields": [],
  "recommendedRoute": "Specialist Queue",
  "reasoning": "Injury-related claim"
}
```

---

## Project Structure

```
super/
│
├── app/
│   ├── main.py        # FastAPI entry point (/process-claim)
│   ├── extractor.py  # FNOL PDF extraction logic
│   ├── router.py     # Claim routing rules
│   ├── models.py     # Response schema
│   └── __init__.py
│
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## Design Rationale

* Rule order ensures safety and compliance first
* Missing data is handled before any automation
* Fraud detection has higher priority than fast-track
* Routing decisions are explainable and auditable

---

## Future Improvements

* Layout-aware extraction for ACORD PDFs
* OCR support for scanned documents
* Confidence scoring per field
* Config-driven routing rules
* AI/NLP-based extraction

---

## Author

Built as an assessment-ready FNOL claims routing system using FastAPI and Python.
