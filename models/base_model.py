#!/bin/usr/python3
"""
This File defines the BaseModel class that will
serve as the base class for all our models."""

from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Base class for all our classes"""

    def __init__(self):
        """constructor"""
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __str__(self):
        """overide str representation of self"""
        fmt = "[{}] ({}) {}"
        return fmt.format(
                type(self).__name__,
                self.id,
                self.__dict__)

    def save(self):
        """updates last updated variable"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Returns a dictionary representation of self"""
        temp = {**self.__dict__}
        temp['__class__'] = type(self).__name__
        temp['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
        temp['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f')
