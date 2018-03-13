from sqlalchemy import Column, BigInteger, ForeignKey, String, DateTime, Integer
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CreatedMixin(object):
    """Created_at mixin"""
    created_at = Column(DateTime, default=datetime.now, nullable=False, server_default="NOW()")


class Camera(Base, CreatedMixin):
    """Camera model"""
    __tablename__ = "cameras"

    id = Column(BigInteger, primary_key=True)
    room_id = Column(
        BigInteger,
        ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    name = Column(String(1000), nullable=False)
    ip = Column(String(1000), nullable=False)
    status = Column(Integer, nullable=False, default=0)
    settings = Column(String(1000))


class RoomEvent(Base, CreatedMixin):
    """Room event model"""

    __tablename__ = "room_events"

    # room events status coode
    STATUS_DONE = "done"
    STATUS_MISSED = "missed"
    STATUS_PLANNED = "planned"
    STATUS_OUT_OF_SCHEDULE = "out_of_schedule"

    EARLY_TERMINATION_NONE = "none"
    EARLY_TERMINATION_NOT_CONFIRMED = "not_confirmed"
    EARLY_TERMINATION_CONFIRMED = "confirmed"

    LATE_BEGINNING_NONE = "none"
    LATE_BEGINNING_NOT_CONFIRMED = "not_confirmed"
    LATE_BEGINNING_CONFIRMED = "confirmed"

    EVENT_STATUS = {
        STATUS_DONE: 0,
        STATUS_MISSED: 1,
        STATUS_PLANNED: 2,
        STATUS_OUT_OF_SCHEDULE: 3
    }

    BEGINNING_STATUS = {
        EARLY_TERMINATION_NONE: 0,
        EARLY_TERMINATION_NOT_CONFIRMED: 1,
        EARLY_TERMINATION_CONFIRMED: 2
    }

    TERMINATION_STATUS = {
        LATE_BEGINNING_NONE: 0,
        LATE_BEGINNING_NOT_CONFIRMED: 1,
        LATE_BEGINNING_CONFIRMED: 2
    }

    id = Column(BigInteger, primary_key=True)
    room_id = Column(
        BigInteger,
        ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_gap = Column(Integer, nullable=False, default=0)
    end_gap = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=0)
    late_beginning = Column(Integer, nullable=False, default=0)
    early_termination = Column(Integer, nullable=False, default=0)
    visitors = Column(Integer, nullable=False, default=0)
    projector_usage = Column(Integer, nullable=False, default=0)
    computer_usage = Column(Integer, nullable=False, default=0)
    visitor_list = Column(String)


class Building(Base, CreatedMixin):
    """Building model"""

    __tablename__ = "buildings"

    id = Column(BigInteger, primary_key=True)
    external_id = Column(String(1000), nullable=False)
    name = Column(String(1000), nullable=False)
    alias = Column(String(1000))
    address = Column(String(1000))

    # relati    ons
    rooms = relationship("Room", cascade="all,delete-orphan", backref="building")



class Room(Base, CreatedMixin):
    """Room model"""

    __tablename__ = "rooms"

    id = Column(BigInteger, primary_key=True)
    external_id = Column(String(1000), nullable=False)
    building_id = Column(
        BigInteger,
        ForeignKey("buildings.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    name = Column(String(1000), nullable=False)
    alias = Column(String(1000))
    settings = Column(String)

    # relations
    cameras = relationship("Camera", cascade="all,delete-orphan", backref="room")
    events = relationship("RoomEvent", cascade="all,delete-orphan", backref="room")
