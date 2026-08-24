from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.disease import DiseaseDiagnosisRequest, DiseaseDiagnosisResponse
from app.services import disease_service

router = APIRouter(prefix="/disease", tags=["Disease Diagnosis"])

@router.post("/diagnose", response_model=DiseaseDiagnosisResponse)
def diagnose_disease(req: DiseaseDiagnosisRequest, db: Session = Depends(get_db)):
    return disease_service.diagnose_crop_disease(db, req)
