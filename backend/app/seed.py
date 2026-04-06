from sqlmodel import Session, select
from .db import get_engine
from .models import Farmer, Plot

def seed():
    engine = get_engine()
    with Session(engine) as s:
        existing = s.exec(select(Farmer)).first()
        if existing:
            print("Seed skipped, data exists")
            return
        f = Farmer(name="Ram", phone="+9198xxxx", language="mr")
        s.add(f)
        s.commit()
        s.refresh(f)
        p = Plot(name="Plot A", area_hectares=1.2, crop="tomato", farmer_id=f.id)
        s.add(p)
        s.commit()
        print("Seed complete. Farmer id:", f.id)

if __name__ == "__main__":
    seed()