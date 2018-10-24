# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *

class PolicyPredicateSqlGroup:
    def __init__(self,
                 Name=None,
                 ):
        self.Name = Name

    @property
    def Name(self): return self._Name

    def dumpToJson(self):
        return {"name": self._
        }