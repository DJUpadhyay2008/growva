from sqlalchemy.orm import Session
from app.database.models import PlannerTaskModel
from app.schemas.planner import PlannerTaskCreate, PlannerTaskResponse, StageStep
from typing import List, Optional

def get_active_tasks(db: Session) -> List[PlannerTaskModel]:
    return db.query(PlannerTaskModel).filter(PlannerTaskModel.is_active == True).all()

def create_planner_task(db: Session, task_in: PlannerTaskCreate) -> PlannerTaskModel:
    task = PlannerTaskModel(
        field_name=task_in.field_name,
        crop_name=task_in.crop_name,
        sowing_date=task_in.sowing_date,
        expected_harvest=task_in.expected_harvest,
        stage_name=task_in.stage_name,
        progress_pct=task_in.progress_pct,
        soil_moisture_pct=task_in.soil_moisture_pct,
        weather_alert=task_in.weather_alert,
        daily_recommendation=task_in.daily_recommendation
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def build_timeline_steps(task: PlannerTaskModel) -> List[StageStep]:
    return [
        StageStep(step_num="01", title="Prepare soil", target_date="This week", done=True),
        StageStep(step_num="02", title="Sowing window", target_date=task.sowing_date, done=task.progress_pct >= 25),
        StageStep(step_num="03", title="First irrigation", target_date="02 Sep", done=task.progress_pct >= 50),
        StageStep(step_num="04", title="Expected harvest", target_date=task.expected_harvest, done=task.progress_pct >= 100),
    ]
