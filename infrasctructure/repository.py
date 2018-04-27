import os
from datetime import date, timedelta
from sqlalchemy import create_engine, text
from domain.model import PhoneCallStart, Base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

connection_string = os.getenv('DATABASE_URL', 'mysql://root:root@database/phone_calls')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
db = SQLAlchemy(app, metadata=Base.metadata)


def find_start_calls_by_phone_number_within_month(year: int, month: int, phone_number: str):
    next_month = month + 1 if month < 12 else 1
    month_start = date(year, month, 1)
    month_end = date(year if month < 12 else year + 1, next_month, 1) - timedelta(days=1)

    return db.session.query(PhoneCallStart) \
        .filter(text('start_timestamp > :month_start')) \
        .filter(text('start_timestamp < :month_end')) \
        .filter(text('source = :phone_number')) \
        .filter(text('cost > 0')) \
        .params(month_start = month_start.isoformat(),
                month_end = month_end.isoformat(),
                phone_number = phone_number) \
        .all()


def find_start_call_by_call_id(call_id: int) -> PhoneCallStart:
    return db.session.query(PhoneCallStart).filter(text('call_id = :call_id')).params(call_id = call_id).one()
