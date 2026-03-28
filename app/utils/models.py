from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base
from app.utils.db import Base

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String, index=True)
    business_direction = Column(String)
    
    date_occurred = Column(DateTime, index=True)
    date_reported = Column(DateTime)
    
    injury_severity = Column(String)
    injured_body_part = Column(String)
    position = Column(String)
    work_type = Column(String)
    
    is_accident = Column(Boolean)
    in_work_hours = Column(Boolean)
    at_workplace = Column(Boolean)
    contractor = Column(String)
    
    preliminary_causes = Column(Text)
    description = Column(Text)
    corrective_measures = Column(Text)


class Korgau(Base):
    __tablename__ = "korgau"
    
    id = Column(Integer, primary_key=True, index=True)
    observation_type = Column(String, index=True)
    category = Column(String)
    
    date_observed = Column(DateTime, index=True)
    time_observed = Column(String)
    org = Column(String, index=True)
    
    stopped_work = Column(Boolean)
    discussed = Column(Boolean)
    reported = Column(Boolean)
    resolved = Column(Boolean)
    
    # Risks
    risk_level = Column(Float)
    critical_alert = Column(Integer)
    
    # Texts
    consequences_or_benefits = Column(Text)
    measures_taken = Column(Text)
