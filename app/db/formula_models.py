import uuid

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
from datetime import datetime



class Formula(Base):
    __tablename__ = 'formulas'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    expression = Column(Text, nullable=False)
    tags = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    runs = relationship("RunSession", back_populates="formula")


class RunSession(Base):
    __tablename__ = 'run_sessions'

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String(50), unique=True, nullable=False)
    input_file = Column(String(255))
    formula_id = Column(Integer, ForeignKey("formulas.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="PENDING")

    formula = relationship("Formula", back_populates="runs")