from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.byproduct import ByProduct, ResidueAnalysisRequest, ResidueAnalysisResponse
from app.services import byproduct_service

router = APIRouter(prefix="/byproducts", tags=["By-Products & Post-Harvest Engine"])

@router.get("", response_model=List[ByProduct])
def list_byproducts(
    search: Optional[str] = Query(None, description="Search term for residue, crop, or application"),
    crop: Optional[str] = Query(None, description="Filter by crop name"),
    category: Optional[str] = Query(None, description="Filter by application category"),
    difficulty: Optional[str] = Query(None, description="Filter by processing difficulty (low, medium, high)")
):
    return byproduct_service.get_all_byproducts(search, crop, category, difficulty)

@router.get("/{byproduct_id}", response_model=ByProduct)
def get_byproduct(byproduct_id: str):
    res = byproduct_service.get_byproduct_by_id(byproduct_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"By-product with id '{byproduct_id}' not found.")
    return res

@router.get("/crop/{crop_name}", response_model=ByProduct)
def get_byproduct_for_crop(crop_name: str):
    return byproduct_service.get_byproduct_by_crop(crop_name)

@router.post("/analyze", response_model=ResidueAnalysisResponse)
def analyze_residue(req: ResidueAnalysisRequest):
    return byproduct_service.analyze_crop_byproduct(req)
