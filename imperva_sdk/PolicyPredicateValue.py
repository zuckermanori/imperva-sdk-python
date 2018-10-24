# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *

class PolicyPredicateValue:
    def __init__(self,
                 Value=None,
                 Schema=None,
                 Database=None,
                 TableName=None,
                 ColumnName=None
                 ):
        self._Value = Value
        self._Schema = Schema
        self._Database = Database
        self._TableName = TableName
        self._ColumnName = ColumnName

    @property
    def Value(self): return self._Value

    @property
    def Schema(self): return self._Schema

    @property
    def Database(self): return self._Database

    @property
    def TableName(self): return self._TableName

    @property
    def ColumnName(self): return self._ColumnName

    def dumpToJson(self):
        return {"value": self._Value,
                "schema": self._Schema,
                "database": self._Database,
                "table-name": self._TableName,
                "column-name": self._ColumnName
        }

    def loadFromJson(self, jsonList):
        self._Value = jsonList['value']
