from pydantic import BaseModel
from typing import Optional, List

class StageStep(BaseModel):
    step_num: str
    title: str
    target_date: str
    done: bool

class PlannerTaskBase(BaseModel):
    field_name: str
    crop_name: str
    sowing_date: str
    expected_harvest: str
    stage_name: str
    progress_pct: int = 0
    soil_moisture_pct: int = 35
    weather_alert: Optional[str] = None
    daily_recommendation: Optional[str] = None

class PlannerTaskCreate(PlannerTaskBase):
    pass

class PlannerTaskResponse(PlannerTaskBase):
    id: int
    is_active: bool
    timeline_steps: Optional[List[StageStep]] = None

    class Config:
        from_attributes = True
