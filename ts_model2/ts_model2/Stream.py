from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stream(Base):
    __tablename__ = 'streams'
    stream_id = Column(Integer, primary_key = True)
    streamer = Column(String(250))
    playlist_url = Column(String(250))
    duration = Column(Float)
    fps_numerator = Column(Integer)
    fps_denominator = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    created = Column(DateTime)
