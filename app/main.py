from fastapi import FastAPI, UploadFile, File
from app.extractor import extract_fields
from app.router import route_claim
from app.models import ClaimResponse
import shutil

app = FastAPI(title="FNOL Claims Processing Agent")

@app.post("/process-claim", response_model=ClaimResponse)
async def process_claim(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract FNOL fields
    fields, missing = extract_fields(file_path)

    # Route the claim
    route, reason = route_claim(fields, missing)

    # Return structured response
    return ClaimResponse(
        extractedFields=fields,
        missingFields=missing,
        recommendedRoute=route,
        reasoning=reason
    )
