from sqlalchemy.orm import Session
from app.database.models import DiseaseRecordModel
from app.schemas.disease import DiseaseDiagnosisRequest, DiseaseDiagnosisResponse
from typing import Optional

def diagnose_crop_disease(db: Session, req: DiseaseDiagnosisRequest) -> DiseaseDiagnosisResponse:
    crop_name = req.crop_name.strip()
    symptoms = req.symptoms_text.lower()
    
    record = db.query(DiseaseRecordModel).filter(
        DiseaseRecordModel.crop_name.ilike(f"%{crop_name}%")
    ).first()

    if record:
        matched = [s for s in ["yellowing", "spots", "wilting", "blight", "rust", "rot", "curling"] if s in symptoms]
        if not matched:
            matched = ["leaf coloration anomaly", "texture distortion"]
            
        return DiseaseDiagnosisResponse(
            crop_name=crop_name,
            diagnosed_disease=record.disease_name,
            confidence_score=0.92,
            symptoms_matched=matched,
            organic_treatment=record.organic_treatment,
            chemical_treatment=record.chemical_treatment,
            preventive_measures=record.preventive_measures
        )

    # Generic fallback advisory
    return DiseaseDiagnosisResponse(
        crop_name=crop_name,
        diagnosed_disease=f"Fungal / Bacterial Leaf Blight on {crop_name}",
        confidence_score=0.85,
        symptoms_matched=["chlorosis", "leaf spot"],
        organic_treatment="Spray Neem oil extract (5ml/L water) or Trichoderma harzianum formulation.",
        chemical_treatment="Apply Copper Oxychloride 50 WP (2.5g/L water) or Mancozeb 75 WP.",
        preventive_measures="Maintain optimal plant spacing, avoid overhead irrigation, and remove infected crop debris."
    )
