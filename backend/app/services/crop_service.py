from sqlalchemy.orm import Session
from app.database.models import CropModel
from typing import List, Optional

def get_crops(
    db: Session,
    category: Optional[str] = None,
    query: Optional[str] = None,
    skip: int = 0,
    limit: int = 120
) -> List[CropModel]:
    q = db.query(CropModel)
    if category and category.lower() != 'all':
        q = q.filter(CropModel.category.ilike(category))
    if query:
        q = q.filter(
            (CropModel.name.ilike(f"%{query}%")) |
            (CropModel.hindi_name.ilike(f"%{query}%")) |
            (CropModel.gujarati_name.ilike(f"%{query}%"))
        )
    return q.offset(skip).limit(limit).all()

def count_crops(db: Session, category: Optional[str] = None, query: Optional[str] = None) -> int:
    q = db.query(CropModel)
    if category and category.lower() != 'all':
        q = q.filter(CropModel.category.ilike(category))
    if query:
        q = q.filter(
            (CropModel.name.ilike(f"%{query}%")) |
            (CropModel.hindi_name.ilike(f"%{query}%")) |
            (CropModel.gujarati_name.ilike(f"%{query}%"))
        )
    return q.count()

def get_crop_by_name(db: Session, name: str) -> Optional[CropModel]:
    return db.query(CropModel).filter(CropModel.name.ilike(name)).first()

def get_crop_by_id(db: Session, crop_id: int) -> Optional[CropModel]:
    return db.query(CropModel).filter(CropModel.id == crop_id).first()
