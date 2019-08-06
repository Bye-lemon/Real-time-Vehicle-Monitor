from sqlalchemy import Column, Integer, Float, TIMESTAMP, Boolean, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pprint

Base = declarative_base()


class RawData(Base):
    """AirSim RawData"""

    __tablename__ = "rawdatas"

    id = Column(Integer, primary_key=True)
    gear = Column(Integer, nullable=False)
    handbreak = Column(Boolean, nullable=False)
    maxrpm = Column(Float, nullable=False)
    rpm = Column(Float, nullable=False)
    speed = Column(Float, nullable=False)
    timestamp = Column(TIMESTAMP(True), nullable=False,
                       server_default=text('NOW()'))
    pos_x = Column(Float, nullable=False)
    pos_y = Column(Float, nullable=False)
    pos_z = Column(Float, nullable=False)
    aa_x = Column(Float, nullable=False)
    aa_y = Column(Float, nullable=False)
    aa_z = Column(Float, nullable=False)
    av_x = Column(Float, nullable=False)
    av_y = Column(Float, nullable=False)
    av_z = Column(Float, nullable=False)
    la_x = Column(Float, nullable=False)
    la_y = Column(Float, nullable=False)
    la_z = Column(Float, nullable=False)
    lv_x = Column(Float, nullable=False)
    lv_y = Column(Float, nullable=False)
    lv_z = Column(Float, nullable=False)

    def __init__(self, gear, handbreak, maxrpm, rpm, speed, pos_x, pos_y, pos_z, aa_x, aa_y, aa_z, av_x,
                 av_y, av_z, la_x, la_y, la_z, lv_x, lv_y, lv_z):
        Base.__init__(self, gear=gear, handbreak=handbreak, maxrpm=maxrpm, rpm=rpm, speed=speed, pos_x=pos_x,
                      pos_y=pos_y, pos_z=pos_z, aa_x=aa_x, aa_y=aa_y, aa_z=aa_z,
                      av_x=av_x, av_y=av_y, av_z=av_z, la_x=la_x, la_y=la_y, la_z=la_z, lv_x=lv_x, lv_y=lv_y,
                      lv_z=lv_z)


engine = create_engine(
    'mysql+pymysql://root:lingying_@cdb-rokmsrpe.bj.tencentcdb.com:10033/CarSim')
DBSession = sessionmaker(bind=engine)


def getData():
    session = DBSession()
    raw_data = session.query(RawData).all()
    return raw_data[-40:] if len(raw_data) > 40 else raw_data
