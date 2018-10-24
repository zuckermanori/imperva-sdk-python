# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *

class PolicyRuleRetentionDefinitions:

    def __init__(self,
                RelativeOrder=None,
                OverrideExistingValues=None,
                Ttl=None,
                TaggingScope=None
                 ):
        self._RelativeOrder = RelativeOrder
        self._OverrideExistingValues = OverrideExistingValues
        self._Ttl = Ttl
        self._TaggingScope = TaggingScope

    @property
    def RelativeOrder(self): return self._RelativeOrder

    @property
    def OverrideExistingValues(self): return self._OverrideExistingValues

    @property
    def Ttl(self): return self._Ttl

    @property
    def TaggingScope(self): return self._TaggingScope

    def dumpToJson(self):
        return {"relative-order": self._RelativeOrder,
            "override-existing-values": self._OverrideExistingValues,
            "ttl": self._Ttl,
            "tagging-scope": self._TaggingScope
        }