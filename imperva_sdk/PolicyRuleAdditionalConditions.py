# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *

class PolicyRuleAdditionalConditions:
    def __init__(self,
                 DiscriminatorIndex=None,
                 DiscriminatorValue=None
                 ):
        self._DiscriminatorIndex = DiscriminatorIndex
        self._DiscriminatorValue = DiscriminatorValue

    @property
    def DiscriminatorIndex(self): return self._DiscriminatorIndex

    @property
    def DiscriminatorValue(self): return self._DiscriminatorValue

    def dumpToJson(self):
        return {
            "discriminator-index": self._DiscriminatorIndex,
            "discriminator-value": self._DiscriminatorValue
        }