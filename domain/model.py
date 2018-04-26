from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import re


Base = declarative_base()


def is_date_within_hour_range(datetime: datetime, start_hour: int, end_hour: int) -> bool:
    return datetime.hour >= start_hour and datetime.hour <= end_hour


class PhoneCallStart(Base):
    __tablename__ = 'phone_call_start'
    __id = Column('id', Integer, primary_key=True)
    __start_timestamp = Column('start_timestamp', DateTime, index=True, nullable=False)
    __end_timestamp = Column('end_timestamp', DateTime, index=True, nullable=True)
    __call_id = Column('call_id', Integer, unique=True, nullable=False)
    __source = Column('source', String(11), index=True, nullable=False)
    __destination = Column('destination', String(11), index=True, nullable=False)
    __cost = Column('cost', Float)

    def __init__(self, timestamp: datetime, call_id: int, source: str, destination: str):
        self.__start_timestamp = timestamp
        self.__call_id = call_id
        self.__source = source
        self.__destination = destination
        self.__cost = 0
        self.__end_timestamp = None
        self.__validate()

    def __validate(self):
        pattern = re.compile('^\d{10,11}$')
        error_message = 'phone numbers must be numbers containing at least 10 digits and max 11'

        assert pattern.match(str(self.__source)), error_message
        assert pattern.match(str(self.__destination)), error_message
        assert self.__start_timestamp is not None, 'call start date is mandatory'
        assert self.__call_id is not None, 'call id is mandatory'

    @property
    def id(self) -> int:
        return self.__id

    @property
    def start_timestamp(self) -> datetime:
        return self.__start_timestamp

    @property
    def call_id(self) -> int:
        return self.__call_id

    @property
    def source(self) -> str:
        return self.__source

    @property
    def destination(self) -> str:
        return self.__destination

    @property
    def end_timestamp(self) -> datetime:
        return self.__end_timestamp

    @end_timestamp.setter
    def end_timestamp(self, end_timestamp: datetime):
        self.__end_timestamp = end_timestamp
        self.__calculate_cost()

    def __calculate_cost(self):
        standing_charge = 0.36
        call_charge = 0.09
        duration = self.__chargeable_call_duration()

        self.__cost = standing_charge + ((duration.seconds / 60) * call_charge) if duration.seconds > 0 \
            else standing_charge

    def __chargeable_call_duration(self) -> timedelta:
        start_date = self.start_timestamp
        end_date = self.end_timestamp

        if is_date_within_hour_range(start_date, 6, 22) or is_date_within_hour_range(end_date, 6, 22):
            if start_date.hour < 6:
                start_date = start_date.replace(hour=6)

            if end_date.hour > 22:
                end_date = end_date.replace(hour=22)

            return end_date - start_date

        return timedelta(seconds=0)

    def is_call_ended(self) -> bool:
        return False if not self.end_timestamp else True

    @property
    def call_duration(self) -> timedelta:
        if not self.is_call_ended():
            raise RuntimeError('Cannot determine call duration before it\'s ended')

        return self.end_timestamp - self.start_timestamp

    @property
    def cost(self) -> float:
        if (not self.__cost):
            raise RuntimeError("cost wasn't determined yet, maybe phone call has not ended")

        return self.__cost