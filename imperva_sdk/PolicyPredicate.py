# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *

from imperva_sdk.PolicyPredicateValue import *
from imperva_sdk.PolicyPredicateFieldGenericGroup import *

class PolicyPredicate:
    def __init__(self,
                PredicateType=None,
                Name=None,
                Operation=None,
                Field=None,
                NumValue = None,
                HandleUnknownValues = None,
                Within = None,
                Times = None,
                Context = None,
                Tag = None,
                SearchMode = None,
                SearchNumericValues = None,
                Values = [],
                GenericGroups = [],
                SqlGroups = []
                ):
        self._PredicateType = PredicateType
        self._Name = Name
        self._Operation = Operation
        self._Field = Field
        self._NumValue = NumValue
        self._HandleUnknownValues = HandleUnknownValues
        self._Within = Within
        self._Times = Times
        self._Context = Context
        self._Tag = Tag
        self._SearchMode = SearchMode
        self._SearchNumericValues = SearchNumericValues

        if type(Values) is list:
            self._Values = []
            for value in Values:
                if type(value).__name__ == 'dict':
                    value = self.validateValueEmptyIndices(value)
                    self._Values.append(PolicyPredicateValue(Value=value['value'], Schema=value['schema'], Database=value['database'],
                                                    TableName=value['table-name'], ColumnName=value['column-name']))
                elif value.__class__.__name__ == 'PolicyPredicateValue':
                    self._Values.append(value)

        if type(GenericGroups) is list:
            self._GenericGroups = []
            for group in GenericGroups:
                if type(group).__name__ == 'dict':
                    group = self.validateGenericGroupsEmptyIndices(group)
                    self._GenericGroups.append(PolicyPredicateFieldGenericGroup(Name=group['name'], Description=group['description']))
                elif group.__class__.__name__ == 'PolicyPredicateFieldGenericGroup':
                    self._GenericGroups.append(group)

        if type(SqlGroups) is list:
            self._SqlGroups = []
            for sqlGroup in SqlGroups:
                sqlGroup = self.validateSqlGroupEmptyIndices(sqlGroup)
                if type(sqlGroup).__name__ == 'dict':
                    self._SqlGroups.append(PolicyPredicateSqlGroup(Name=sqlGroup['name']))
                elif sqlGroup.__class__.__name__ == 'PolicyPredicateSqlGroup':
                    self._SqlGroups.append(sqlGroup)

    @property
    def PredicateType(self): return self._PredicateType

    @property
    def Name(self): return self._Name

    @property
    def Operation(self): return self._Operation

    @property
    def Field(self): return self._Field

    @property
    def NumValue(self): return self._NumValue

    @property
    def HandleUnknownValues(self): return self._HandleUnknownValues

    @property
    def Within(self): return self._Within

    @property
    def Times(self): return self._Times

    @property
    def Context(self): return self._Context

    @property
    def Tag(self): return self._Tag

    @property
    def SearchMode(self): return self._SearchMode

    @property
    def SearchNumericValues(self): return self._SearchNumericValues

    @property
    def Values(self):
        return self._Values

    @property
    def GenericGroups(self):
        return self._GenericGroups

    @property
    def SqlGroups(self):
        return self._SqlGroups

    def dumpToJson(self):
        jsonObj = {"type": self._PredicateType,
            "name": self._Name,
            "operation": self._Operation,
            "field": self._Field,
            "num-value": self._NumValue,
            "handle-unknown-values": self._HandleUnknownValues,
            "within": self._Within,
            "times": self._Times,
            "context": self._Context,
            "tag": self._Tag,
            "search-mode": self._SearchMode,
            "search-numeric-values": self._SearchNumericValues
        }

        if hasattr(self, '_Values') and type(self._Values) is list:
            jsonValues = []
            for value in self._Values:
                if not value is None and value.__class__.__name__ is 'PolicyPredicateValue':
                    jsonValues.append(value.dumpToJson())
            jsonObj["values"] = jsonValues

        if hasattr(self, '_GenericGroups') and type(self._GenericGroups) is list:
            jsonGroups = []
            for group in self._GenericGroups:
                if not group is None and group.__class__.__name__ is 'PolicyPredicateFieldGenericGroup':
                    jsonGroups.append(group.dumpToJson())
            jsonObj["generic-groups"] = jsonGroups

        if hasattr(self, '_SqlGroups') and type(self._SqlGroups) is list:
            jsonSqlGroups = []
            for sqlGroup in self._SqlGroups:
                if not sqlGroup is None and sqlGroup.__class__.__name__ is 'PolicyPredicateSqlGroup':
                    jsonSqlGroups.append(sqlGroup.dumpToJson())
            jsonObj["sql-groups"] = jsonSqlGroups

        return jsonObj

    @staticmethod
    def validateValueEmptyIndices(value):
        if not type(value).__name__ == 'dict':
            return value

        if not 'value' in value:
            value['value'] = None
        if not 'schema' in value:
            value['schema'] = None
        if not 'database' in value:
            value['database'] = None
        if not 'table-name' in value:
            value['table-name'] = None
        if not 'column-name' in value:
            value['column-name'] = None

        return value

    @staticmethod
    def validateGenericGroupsEmptyIndices(group):
        if not type(group).__name__ == 'dict':
            return group

        if not 'name' in group:
            group['name'] = None
        if not 'description' in group:
            group['description'] = None

        return group

    @staticmethod
    def validateSqlGroupEmptyIndices(sqlGroup):
        if not type(sqlGroup).__name__ == 'dict':
            return sqlGroup

        if not '' in sqlGroup:
            sqlGroup[''] = None

        return sqlGroup