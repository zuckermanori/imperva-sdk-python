# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *

class PolicyRuleGenericGroups:
    def __init__(self,
                 SourceEventField=None,
                 LookupDataSet=None,
                 Attribute=None
                 ):
        self._SourceEventField = SourceEventField
        self._LookupDataSet = LookupDataSet
        self._Attribute = Attribute

    @property
    def SourceEventField(self): return self._SourceEventField

    @property
    def LookupDataSet(self): return self._LookupDataSet

    @property
    def Attribute(self): return self._Attribute

    def dumpToJson(self):
        return {"source-event-field": self._SourceEventField,
	            "lookup-data-set": self._LookupDataSet,
	            "attribute": self.Attribute
        }