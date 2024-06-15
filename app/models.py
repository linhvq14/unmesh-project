from . import db


class Device(db.Model):
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), index=True, unique=True)

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

    # Add other columns relevant to the user table

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'last_name': self.last_name,
            # Add other fields here
        }
