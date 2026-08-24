from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.planner import PlannerTaskCreate, PlannerTaskResponse
from app.services import planner_service
from typing import List

router = APIRouter(prefix="/planner", tags=["Planner"])

@router.get("/tasks", response_model=List[PlannerTaskResponse])
def get_planner_tasks(db: Session = Depends(get_db)):
    tasks = planner_service.get_active_tasks(db)
    res = []
    for t in tasks:
        item = PlannerTaskResponse.from_orm(t)
        item.timeline_steps = planner_service.build_timeline_steps(t)
        res.append(item)
    return res

@router.post("/tasks", response_model=PlannerTaskResponse)
def create_planner_task(task_in: PlannerTaskCreate, db: Session = Depends(get_db)):
    task = planner_service.create_planner_task(db, task_in)
    res = PlannerTaskResponse.from_orm(task)
    res.timeline_steps = planner_service.build_timeline_steps(task)
    return res
