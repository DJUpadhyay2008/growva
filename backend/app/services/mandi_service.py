from sqlalchemy.orm import Session
from app.database.models import MandiPriceModel
from typing import List, Optional

def get_mandi_prices(
    db: Session,
    commodity: Optional[str] = None,
    state: Optional[str] = None,
    market: Optional[str] = None,
    limit: int = 50
) -> List[MandiPriceModel]:
    q = db.query(MandiPriceModel)
    if commodity:
        q = q.filter(MandiPriceModel.commodity.ilike(f"%{commodity}%"))
    if state:
        q = q.filter(MandiPriceModel.state.ilike(f"%{state}%"))
    if market:
        q = q.filter(MandiPriceModel.market.ilike(f"%{market}%"))
    return q.limit(limit).all()

def count_mandi_prices(db: Session, commodity: Optional[str] = None) -> int:
    q = db.query(MandiPriceModel)
    if commodity:
        q = q.filter(MandiPriceModel.commodity.ilike(f"%{commodity}%"))
    return q.count()
