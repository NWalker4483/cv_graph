class Detection():
    def __init__(self, id = 0, bbox = [(0,0), (1,1)], frame = 0, category = "unknown"):
        pass
    # TODO Look into python datamodels

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Detection(Base):
    __tablename__ = 'detections'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    frame_num = Column(Integer, nullable=False)
    bbox = Column(String(250), nullable=False)
    category = Column(String(250), nullable=True)