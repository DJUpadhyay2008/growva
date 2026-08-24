import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.database.database import SessionLocal
from app.database.models import MandiPriceModel

db = SessionLocal()

mandi_data = [
      ("Gujarat", "Banaskantha", "Deesa APMC", "Castor Seed", "Gujarat Castor", 5200.0, 5800.0, 5600.0, "2026-08-24"),
      ("Gujarat", "Bhavnagar", "Mahuva APMC", "Bajra", "Desi", 2000.0, 2400.0, 2200.0, "2026-08-24"),
      ("Punjab", "Amritsar", "Amritsar Mandi", "Wheat", "HD 2967", 2200.0, 2400.0, 2350.0, "2026-08-24"),
      ("Punjab", "Bathinda", "Bathinda Mandi", "Cotton", "Bt Cotton", 6500.0, 7100.0, 6900.0, "2026-08-24"),
      ("Punjab", "Patiala", "Patiala APMC", "Mustard", "Sarson", 4800.0, 5400.0, 5100.0, "2026-08-24"),
      ("Punjab", "Jalandhar", "Jalandhar Mandi", "Maize", "Hybrid", 2100.0, 2500.0, 2300.0, "2026-08-24"),
      ("Punjab", "Fazilka", "Abohar Mandi", "Kinnow", "Grade A", 1800.0, 2600.0, 2200.0, "2026-08-24"),
      ("Maharashtra", "Pune", "Pune APMC", "Sugarcane", "Co 86032", 280.0, 320.0, 300.0, "2026-08-24"),
      ("Maharashtra", "Latur", "Latur Mandi", "Soybean", "JS 335", 4500.0, 5100.0, 4800.0, "2026-08-24"),
      ("Maharashtra", "Sangli", "Sangli APMC", "Turmeric", "Rajapuri", 12000.0, 15500.0, 14000.0, "2026-08-24"),
      ("Maharashtra", "Solapur", "Solapur Mandi", "Pomegranate", "Bhagwa", 6000.0, 9000.0, 7500.0, "2026-08-24"),
      ("Maharashtra", "Jalgaon", "Jalgaon APMC", "Cotton", "MCU-5", 6700.0, 7300.0, 7000.0, "2026-08-24")
]

for m in mandi_data:
    existing = db.query(MandiPriceModel).filter_by(market=m[2], commodity=m[3]).first()
    if not existing:
        mandi = MandiPriceModel(
            state=m[0], district=m[1], market=m[2],
            commodity=m[3], variety=m[4],
            min_price=m[5], max_price=m[6], modal_price=m[7],
            arrival_date=m[8]
        )
        db.add(mandi)

db.commit()
db.close()
print("Added extra mandi prices.")
