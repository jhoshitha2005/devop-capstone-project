"""
Models for Account
"""

import logging
from datetime import date
from service import db

logger = logging.getLogger("flask.app")

class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""

class Account(db.Model):
    """Class that represents an Account"""

    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(32), nullable=True)  # optional
    date_joined = db.Column(db.Date(), nullable=False, default=date.today)

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        """Serialize an Account into a dict"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None
        }

    def deserialize(self, data):
        """Deserialize Account from dict"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
            date_joined = data.get("date_joined")
            if date_joined:
                self.date_joined = date.fromisoformat(date_joined)
            else:
                self.date_joined = date.today()
        except KeyError as error:
            raise DataValidationError(f"Invalid Account: missing {error.args[0]}") from error
        except TypeError as error:
            raise DataValidationError(f"Invalid Account: bad data - {error.args[0]}") from error
        return self

    @classmethod
    def find_by_name(cls, name):
        """Return all Accounts matching the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).all()

