# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *

class PolicyPredicateFieldGenericGroup:
    def __init__(self,
                 Name=None,
                 Description=None
                 ):
        self._Name = Name
        self._Description = Description

    @property
    def Name(self): return self._Name

    @property
    def Description(self): return self._Description

    def dumpToJson(self):
        return {"name": self._Name,
                "description": self._Description,
        }