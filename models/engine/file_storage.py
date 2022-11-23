#!/usr/bin/python3
"""
This File defines the storage system (File System)
For the project.
It uses json format to serialize or deserialize
an object"""

import json
from models.base_model import BaseModel
from .errors import *
from datetime import datetime


class FileStorage:
    """This class serve as an ORM to interface between or Storage System"""

    # class private variables
    __objects: dict = {}
    __file_path: str = "file.json"
    models = {
            "BaseModel":BaseModel
    }

    def __init__(self, fname=None):
        """constructor"""
        pass

    def all(self):
        """Return all instances stored"""
        return FileStorage.__objects

    def new(self, obj):
        """Stores a new Object"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes objects stored and persist in file"""
        serialized = list(map(
            lambda obj: obj.to_dict(),
            FileStorage.__objects.values()))
        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(serialized))

    def reload(self):
        """de-serialize persisted objects"""
        try:
            deserialized = []
            with open(FileStorage.__file_path, "r") as f:
                deserialized = json.loads(f.read())
            FileStorage.__objects = {
                    obj["__class__"] + "." + obj["id"]:
                    FileStorage.models[obj["__class__"]](**obj)
                    for obj in deserialized}
        except FileNotFoundError:
            # No need for error
            pass

    def find_by_id(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in F.models:
            # Invalid Model Name
            # Not yet Implemented
            raise ModelNotFoundError(model)

        key = model + "." + obj_id
        if key not in F.__objects:
            # invalid id
            # Not yet Implemented
            raise InstanceNotFoundError(obj_id, model)

        return F.__objects[key]

    def delete_by_id(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in F.models:
            raise ModelNotFoundError(model)

        key = model + "." + obj_id
        if key not in F.__objects:
            raise InstanceNotFoundError(obj_id, model)

        del F.__objects[key]
        self.save()

    def find_all(self, model=""):
        """Find all instances or instances of model"""
        if model and model not in FileStorage.models:
            raise ModelNotFoundError(model)
        results = []
        for key, val in FileStorage.__objects.items():
            if key.startswith(model):
                results.append(str(val))
        return results

    def update_one(self, model, iid, field, val):
        """Updates an instance"""
        F = FileStorage
        if model not in F.models:
            raise ModelNotFoundError(model)

        key = model + "." + iid
        if key not in F.__objects:
            raise InstanceNotFoundError(iid, model)
        if field in ("id", "updated_at", "created_at"):
            # not allowed to be updated
            return
        inst = F.__objects[key]
        try:
            # if instance has that value
            # cast it to its type
            vtype = type(inst.__dict__[field])
            inst.__dict__[field] = vtype(val)
        except KeyError:
            # instance doesn't has the field
            # assume type of string
            inst.__dict__[field] = str(val)
        finally:
            inst.updated_at = datetime.utcnow()
            self.save()
