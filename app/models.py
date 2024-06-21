from datetime import datetime

from . import db


class Device(db.Model):
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)

    # Add other columns relevant to the device table

    def to_dict(self):
        return {
            'device_id': self.device_id,
            # 'name': self.name,
            # Add other fields here
        }


class User(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    phone_number = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)

    # Add other columns relevant to the user table

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'phone_number': self.phone_number,
            'email': self.email,
            'last_name': self.last_name,
            # Add other fields here
        }


class Configure(db.Model):
    __tablename__ = 'configure'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_key = db.Column(db.String(255), unique=True, nullable=False)
    config_value = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
