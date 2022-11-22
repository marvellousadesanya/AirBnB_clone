#!/usr/bin/python3

"""This file defines the console class which will
serve as the entry point of the entire project
"""
from cmd import Cmd
from models import storage

# Global variable of registered models
classes = type(storage).models


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
        """Create an instance of Model given its name
        Example
        $ create ModelName
        Throws an Error if ModelName is missing or doesnt exist"""
        args = parse(args)
        n = len(args)

        if not n:
            print("** class name missing **")
        elif n > 1:
            # Not decided
            pass
        elif args[0] not in classes:
            print("** class doesn't exist **")
        else:
            temp = classes[args[0]]()
            print(temp.id)
            temp.save()


def parse(line: str):
    """splits a line by spaces"""
    return line.split()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
