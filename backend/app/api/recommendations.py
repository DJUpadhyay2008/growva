from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("", response_model=RecommendationResponse)
def get_crop_recommendations(req: RecommendationRequest, db: Session = Depends(get_db)):
    return recommendation_service.generate_crop_recommendations(db, req)
