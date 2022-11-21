#!/usr/bin/python3
"""
This File defines the storage system (File System)
For the project.
It uses json format to serialize or deserialize
an object"""

import json
from models.base_model import BaseModel


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
            pass
