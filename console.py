#!/usr/bin/python3

"""This file defines the console class which will
serve as the entry point of the entire project
"""
from cmd import Cmd
from models import storage
from models.engine.errors import *
import shlex
from models.base_model import BaseModel
from models.user import User


# Global variable of registered models
classes = storage.models


class HBNBCommand(Cmd):
    """
    The Console based driver of the AirBnb Clone
    All interactions with the system is done via
    this class"""

    prompt = "(hbnb) "

    """Commands"""
    def do_EOF(self, args):
        """Exit the programm"""
        return True

    def do_quit(self, args):
        """Quit command exit the program"""
        return True

    def do_create(self, args):
        """Create an instance of Model given its name eg.
        $ create ModelName
        Throws an Error if ModelName is missing or doesnt exist"""
        args, n = parse(args)

        if not n:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif n == 1:
            # temp = classes[args[0]]()
            temp = eval(args[0])()
            print(temp.id)
            temp.save()
        else:
            print("** Too many argument for create **")
            pass

    def do_show(self, arg):
        """Show an Instance of Model base on its ModelName and id eg.
        $ show MyModel instance_id
        Print error message if either MyModel or instance_id is missing
        Print an Error message for wrong MyModel or instance_id"""
        args, n = parse(arg)

        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                inst = storage.find_by_id(*args)
                print(inst)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for show **")
            pass

    def do_destroy(self, arg):
        """Deletes an Instance of Model base on its ModelName and id eg.
        $ destroy MyModel instance_id
        Print error message if either MyModel or instance_id is missing
        Print an Error message for wrong MyModel or instance_id"""
        args, n = parse(arg)

        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            try:
                storage.delete_by_id(*args)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for destroy **")
            pass

    def do_all(self, args):
        """Retrieve all instances: eg.
        $ all
        $ all MyModel
        if MyModel is passed returns only instances of MyModel"""
        args, n = parse(args)

        if n < 2:
            try:
                print(storage.find_all(*args))
            except ModelNotFoundError:
                print("** class doesn't exist **")
        else:
            print("** Too many argument for all **")
            pass

    def do_update(self, arg):
        """Updates an instance base on its id eg
        $ update Model id field value
        Throws errors for missing arguments"""
        args, n = parse(arg)
        if not n:
            print("** class name missing **")
        elif n == 1:
            print("** instance id missing **")
        elif n == 2:
            print("** attribute name missing **")
        elif n == 3:
            print("** value missing **")
        else:
            try:
                storage.update_one(*args[0:4])
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")


def parse(line: str):
    """splits a line by spaces"""
    args = shlex.split(line)
    return args, len(args)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
