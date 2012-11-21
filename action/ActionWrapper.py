import sys
import inspect
from exceptions import *
from env.enums import OperatingSystem, Architecture

"""
Action object which represents a basic action wrapper
"""
class ActionWrapper:
    
    # The data for the Action
    data = None
    
    # The type of this action
    type = None
    
    # Description of the action
    description = ""
    
    # Conditions of the action
    conditions = None
    
    # Whether action is on by default
    default = False
    
    # The OS in use
    os = None
    
    # The architecture in use
    arch = None
    
    """
    Helper function which loads all the classes in this module,
    searches for ones with getType methods, and tries to find the
    one that matches the type given as input, returning an instance
    of it
    """
    def getClass(self, desiredType):
        clazzes = inspect.getmembers(sys.modules["actions"], inspect.isclass)
        for clazzdef in clazzes:
            clazz = clazzdef[1]
            obj = clazz(OperatingSystem.LIN, Architecture.x64)
            try:
                attr = getattr(obj, "getType")
                if callable(attr):
                    clazztype = obj.getType()
                    if clazztype == desiredType:
                        return obj
            except:
                pass
        raise ActionNotFoundException("Unable to load action for type %s" % desiredType)
    
    """
    Load our data from the object into the class
    """
    def load(self):
        print self.data
        try:
            self.type = self.getClass(self.data["Type"])
            self.type.loadProperties(self.data["Properties"])
            if "Description" in self.data:
                self.description = self.data["Description"]
            self.properties = self.data["Properties"]
            if "Conditions" in self.data:
                self.conditions = self.data["Conditions"]
            if "Default" in self.data:
                self.default = self.data["Default"]
        except KeyError as e:
            raise ActionDataMissingException("Unable to find the required key %s" % e)
    
    def __init__(self, os, arch, data = None):
        if data != None:
            self.data = data
            self.os = os
            self.arch = arch
            self.load()