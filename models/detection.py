from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class Detection(Base):
    __tablename__ = 'detections'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    detection_num = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=True )
    frame_num = Column(Integer, nullable=False)
    
    x1 = Column(Integer, nullable=False)
    
    y1 = Column(Integer, nullable=False)
    
    x2 = Column(Integer, nullable=False)
    
    y2 = Column(Integer, nullable=False)

    category = Column(String(250), nullable=True)