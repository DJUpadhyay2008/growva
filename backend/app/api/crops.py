from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.crop import CropResponse, CropListResponse
from app.services import crop_service
from typing import Optional

router = APIRouter(prefix="/crops", tags=["Crops"])

@router.get("", response_model=CropListResponse)
def list_crops(
    category: Optional[str] = Query(None, description="Filter by group (Crops, Pulses, Vegetables, Fruits, Spices)"),
    search: Optional[str] = Query(None, description="Search term for crop name in English, Hindi, or Gujarati"),
    skip: int = Query(0, ge=0),
    limit: int = Query(120, ge=1, le=200),
    db: Session = Depends(get_db)
):
    items = crop_service.get_crops(db, category=category, query=search, skip=skip, limit=limit)
    total = crop_service.count_crops(db, category=category, query=search)
    return CropListResponse(
        total=total,
        showing=len(items),
        items=[CropResponse.from_orm(item) for item in items]
    )

@router.get("/{crop_id}", response_model=CropResponse)
def get_crop_details(crop_id: int, db: Session = Depends(get_db)):
    crop = crop_service.get_crop_by_id(db, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return CropResponse.from_orm(crop)
