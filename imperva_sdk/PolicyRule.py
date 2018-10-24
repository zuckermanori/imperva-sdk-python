# Copyright 2018 Imperva. All rights reserved.

from imperva_sdk.core import *
from imperva_sdk.PolicyRuleRetentionDefinitions import *
from imperva_sdk.PolicyRuleAdditionalConditions import *
from imperva_sdk.PolicyRuleGenericGroups import *

class PolicyRule:

    def __init__(self,
    RuleType=None,
    Order=None,
    TargetFieldName=None,
    TargetField=None,
    Enabled=None,
    ExtractionMethod=None,
    Query=None,
    ValueIndex=None,
    Operation=None,
    TransformValueMatchPattern=None,
    TransformValueReplacementPattern=None,
    RetentionDefinitions=None,
    AdditionalConditions=None,
    Groups=None):
        self._RuleType = RuleType
        self._Order = Order
        self._TargetFieldName = TargetFieldName
        self._TargetField = TargetField
        self._Enabled = Enabled
        self._ExtractionMethod = ExtractionMethod
        self._Query = Query
        self._ValueIndex = ValueIndex
        self._Operation = Operation
        self._TransformValueMatchPattern = TransformValueMatchPattern
        self._TransformValueReplacementPattern = TransformValueReplacementPattern
        if RetentionDefinitions is not None:
            if type(RetentionDefinitions).__name__ == 'dict':
                RetentionDefinitions = self.validateRetentionDefinitionsEmptyIndices(RetentionDefinitions)
                self._RetentionDefinitions = PolicyRuleRetentionDefinitions(RelativeOrder=RetentionDefinitions['relative-order'],
                    OverrideExistingValues=RetentionDefinitions['override-existing-values'],
                    Ttl=RetentionDefinitions['ttl'],
                    TaggingScope=RetentionDefinitions['tagging-scope'])
            elif RetentionDefinitions.__class__.__name__ == 'PolicyRuleRetentionDefinitions':
                self._RetentionDefinitions = RetentionDefinitions

        if AdditionalConditions is not None:
            if type(AdditionalConditions).__name__ == 'dict':
                AdditionalConditions = self.validateAdditionalConditionsEmptyIndices(AdditionalConditions)
                self._AdditionalConditions = PolicyRuleAdditionalConditions(DiscriminatorIndex=AdditionalConditions['discriminator-index'],
                                                                            DiscriminatorValue=AdditionalConditions['discriminator-value'])

            elif AdditionalConditions.__class__.__name__ == 'PolicyRuleAdditionalConditions':
                self._AdditionalConditions = AdditionalConditions

        if Groups is not None:
            if type(Groups).__name__ == 'dict':
                Groups = self.validateGroupsEmptyIndices(Groups)
                self._Groups = PolicyRuleGenericGroups(SourceEventField=Groups['source-event-field'], LookupDataSet=Groups['lookup-data-set'],
                                                       Attribute=Groups['attribute'])
            elif Groups.__class__.__name__ == 'PolicyRuleGenericGroups':
                self._Groups = Groups

    @property
    def RuleType(self): return self._RuleType

    @property
    def Order(self): return self._Order

    @property
    def TargetFieldName(self): return self._TargetFieldName

    @property
    def TargetField(self): return self._TargetField

    @property
    def Enabled(self): return self._Enabled

    @property
    def ExtractionMethod(self): return self._ExtractionMethod

    @property
    def Query(self): return self._Query

    @property
    def ValueIndex(self): return self._ValueIndex

    @property
    def Operation(self): return self._Operation

    @property
    def TransformValueMatchPattern(self): return self._TransformValueMatchPattern

    @property
    def TransformValueReplacementPattern(self): return self._TransformValueReplacementPattern

    @property
    def RetentionDefinitions(self): return self._RetentionDefinitions

    @property
    def AdditionalConditions(self): return self._AdditionalConditions

    @property
    def Groups(self): return self._Groups

    def dumpToJson(self):
        jsonObj = {"type": self._RuleType,
         "order": self._Order,
         "target-field-name": self._TargetFieldName,
         "target-field": self._TargetField,
         "enabled": self._Enabled,
         "extraction-method": self._ExtractionMethod,
         "query": self._Query,
         "value-index": self._ValueIndex,
         "operation": self._Operation,
         "transform-value-match-pattern": self._TransformValueMatchPattern,
         "transform-value-replacement-pattern": self._TransformValueReplacementPattern
        }

        if hasattr(self, '_RetentionDefinitions') and self._RetentionDefinitions.__class__.__name__ is 'PolicyRuleRetentionDefinitions':
            jsonObj["retention-definitions"] = self._RetentionDefinitions.dumpToJson()

        if hasattr(self, '_AdditionalConditions') and self._AdditionalConditions.__class__.__name__ is "PolicyRuleAdditionalConditions":
            jsonObj["additional-conditions"] = self._AdditionalConditions.dumpToJson()

        if hasattr(self, '_Groups') and self._Groups.__class__.__name__ is 'PolicyRuleGenericGroups':
            jsonObj["groups"] = self._Groups.dumpToJson()

        return jsonObj

    @staticmethod
    def validateRetentionDefinitionsEmptyIndices(definitions):
        if not type(definitions).__name__ == 'dict':
            return definitions

        if 'relative-order' not in definitions:
            definitions['relative-order'] = None
        if 'override-existing-values' not in definitions:
            definitions['override-existing-values'] = None
        if 'ttl' not in definitions:
            definitions['ttl'] = None
        if 'tagging-scope' not in definitions:
            definitions['tagging-scope'] = None

        return definitions


    @staticmethod
    def validateAdditionalConditionsEmptyIndices(conditions):
        if not type(conditions).__name__ == 'dict':
            return conditions

        if 'discriminator-index' not in conditions:
            conditions['discriminator-index'] = None
        if 'discriminator-value' not in conditions:
            conditions['discriminator-value'] = None

        return conditions

    @staticmethod
    def validateGroupsEmptyIndices(group):
        if not type(group).__name__ == 'dict':
            return group

        if 'source-event-field' not in group:
            group['source-event-field'] = None
        if 'lookup-data-set' not in group:
            group['lookup-data-set'] = None
        if 'attribute' not in group:
            group['attribute'] = None

        return group