# Copyright 2018 Imperva. All rights reserved.

import json
from imperva_sdk.core import *
from imperva_sdk.PolicyRule                  import *
from imperva_sdk.PolicyPredicate                  import *
from imperva_sdk.PolicyRuleRetentionDefinitions                  import *
from imperva_sdk.PolicyRuleAdditionalConditions                  import *
from imperva_sdk.PolicyRuleGenericGroups                  import *
from imperva_sdk.PolicyPredicateValue                  import *
from imperva_sdk.PolicyPredicateFieldGenericGroup import *

import sys

class DataEnrichmentPolicy(MxObject):
    '''
    MX Data Erichment Policy Class
    '''

    # Store created DB Audit Policy objects in _instances to prevent duplicate instances and redundant API calls
    def __new__(Type, *args, **kwargs):
        obj_exists = DataEnrichmentPolicy._exists(connection=kwargs['connection'], Name=kwargs['Name'])
        if obj_exists:
            return obj_exists
        else:
            obj = super(MxObject, Type).__new__(Type)
            kwargs['connection']._instances.append(obj)
            return obj

    @staticmethod
    def _exists(connection=None, Name=None):
        for curr_obj in connection._instances:
            if type(curr_obj).__name__ == 'DataEnrichmentPolicy':
                if curr_obj.Name == Name:
                    return curr_obj
        return None
    #
    def __init__(self, connection=None, Name=None,
        Rules = [],
        MatchCriteria=[], ApplyTo=[]):

        super(DataEnrichmentPolicy, self).__init__(connection=connection, Name=Name)

        self._Rules = []
        if type(Rules) is list:
            for rule in Rules:
                if not rule is None:
                    if type(rule).__name__ == 'dict':
                        rule = self.validateRuleEmptyIndices(rule)
                        self._Rules.append(PolicyRule(RuleType=rule['type'], Order=rule['order'], TargetFieldName=rule['target-field-name'],
                                                    TargetField=rule['target-field'], Enabled=rule['enabled'],
                                                    ExtractionMethod=rule['extraction-method'],
                                                    Query=rule['query'], ValueIndex=rule['value-index'], Operation=rule['operation'],
                                                    TransformValueMatchPattern=rule['transform-value-match-pattern'],
                                                    TransformValueReplacementPattern=rule['transform-value-replacement-pattern'],
                                                    RetentionDefinitions=rule['retention-definitions'],
                                                    AdditionalConditions=rule['additional-conditions'],
                                                    Groups=rule['groups']))

                    elif rule.__class__.__name__ == 'PolicyRule':
                        self._Rules.append(rule)

        self._MatchCriteria = []
        if type(MatchCriteria) is list:
            for predicate in MatchCriteria:
                if not predicate is None:
                    if type(predicate).__name__ == 'dict':

                        predicate = self.validatePredicateEmptyIndices(predicate)
                        self._MatchCriteria.append(PolicyPredicate(PredicateType=predicate['type'], Name=predicate['name'],
                                        Operation=predicate['operation'], Field=predicate['field'],
                                        NumValue=predicate['num-value'],
                                        HandleUnknownValues=predicate['handle-unknown-values'],
                                        Within=predicate['within'],
                                        Times=predicate['times'], Context=predicate['context'], Tag=predicate['tag'],
                                        SearchMode=predicate['search-mode'],
                                        SearchNumericValues=predicate['search-numeric-values'],
                                        Values=predicate['values'], GenericGroups=predicate['generic-groups'],
                                        SqlGroups=predicate['sql-groups']))

                    elif predicate.__class__.__name__ == 'PolicyPredicate':
                        self._MatchCriteria.append(predicate)
        self._ApplyTo = MxList(ApplyTo)

    # Method: __iter__
    #-----------------------------------------------------------------------------------------------------
    # Description: Override the MxObject __iter__ function to print ApplyTo objects as dictionaries
    #-----------------------------------------------------------------------------------------------------
    #
    def __iter__(self):
        iters = {}
        for field in dir(self):
            if is_parameter.match(field):
                variable_function = getattr(self, field)
                iters[field] = variable_function
        for x, y in iters.items():
            yield x, y

    # Policy Parameter getters
    #-----------------------------------------------------------------------------------------------------
    # Description: properties for all policy parameters
    #-----------------------------------------------------------------------------------------------------
    #
    @property
    def Name                  (self): return self._Name
    @property
    def Rules                 (self): return self._Rules
    @property
    def ApplyTo               (self): return self._ApplyTo
    @property
    def MatchCriteria         (self): return self._MatchCriteria

    @Rules.setter
    def Rules(self, Rules):
        ruleDictObjs = []
        for rule in Rules:
            ruleDictObj = { "type": rule.RuleType,
                            "order": rule.Order,
                            "target-field-name": rule.TargetFieldName,
                            "target-field": rule.TargetField,
                            "enabled": rule.Enabled,
                            "extraction-method": rule.ExtractionMethod,
                            "query": rule.Query,
                            "value-index": rule.ValueIndex,
                            "operation": rule.Operation,
                            "transform-value-match-pattern": rule.TransformValueMatchPattern,
                            "transform-value-replacement-pattern": rule.TransformValueReplacementPattern,
                            "retention-definitions": rule.RetentionDefinitions,
                            "additional-conditions": rule.AdditionalConditions,
                            "groups": rule.Groups
                    }
            ruleDictObjs.append(ruleDictObj)
        self._Rules = ruleDictObjs

    #
    # Data Enrichment policy internal functions
    #
    @staticmethod
    def _get_all_data_enrichment_policies(connection):
        try:
            policyNames = connection._mx_api('GET', '/conf/dataEnrichmentPolicies')
        except:
            raise MxException("Failed getting Data Enrichment Policies")
        policyObjects = []
        for policyName in policyNames:
            # Bug - we have policies with '/' character that don't work with the API...
            if '/' in policyName:
                print("%s cannot be used by the API. Skipping..." % policyName)
                continue
            try:
                policy = connection._mx_api('GET', '/conf/dataEnrichmentPolicies/' + policyName)
            except:
                raise MxException("Failed getting Data Enrichment Policy '%s'" % policyName)
            policyObj = DataEnrichmentPolicy(Name=policy['name'], Rules=None, ApplyTo=None, MatchCriteria=None)
            policyObjects.append(policyObj)
        return policyObjects

    @staticmethod
    def _get_data_enrichment_policy(connection, Name=None):
        validate_string(Name=Name)
        obj_exists = DataEnrichmentPolicy._exists(connection=connection, Name=Name)
        if obj_exists:
            return obj_exists
        try:
            policy = connection._mx_api('GET', '/conf/dataEnrichmentPolicies/' + Name)
        except:
            raise MxException("Failed getting Data Enrichment Policy '%s'" % Name)

        return DataEnrichmentPolicy(connection=connection, Name=policy['policy-name'], Rules=policy['rules'],
                                    MatchCriteria=policy['match-criteria'], ApplyTo=policy['apply-to'])


    @staticmethod
    def _create_data_enrichment_policy(connection, Name=None, PolicyType=None, Rules=[], MatchCriteria=[], ApplyTo=[]):
        validate_string(Name=Name)
        body = {}
        body['policy-name'] = Name
        body['policy-type'] = PolicyType

        applyToStrs = []
        applyToObjs = []
        for curr_apply in ApplyTo:
            if not curr_apply is None:
                applyStr = None
                applyToObj = None
                if type(curr_apply).__name__ == 'dict':
                    applyToObj = curr_apply
                    applyStr = curr_apply['site'] + curr_apply['serverGroup'] + curr_apply['service']
                elif type(curr_apply).__name__ == 'str' and curr_apply.count('/') == 2:
                    applyToObj['site'],parts['serverGroup'],parts['service'] = curr_apply.split('/')
                    applyStr = curr_apply

                if not applyStr is None:
                    applyToStrs.append(applyStr)

                if not applyToObj is None:
                    applyToObjs.append(applyToObj)

        body['apply-to'] = applyToStrs

        ruleDicts = []
        ruleObjs = []
        for rule in Rules:
            if not rule is None:
                ruleDict = None
                ruleObj = None
                if type(rule).__name__ == 'dict':
                    rule = validateRuleEmptyIndices(rule)
                    ruleDict = rule
                    ruleObj = PolicyRule(RuleType=rule['type'], Order=rule['order'], TargetFieldName=rule['target-field-name'],
                                         TargetField=rule['target-field'], Enabled=rule['enabled'], ExtractionMethod=rule['extraction-method'],
                                         Query=rule['query'], ValueIndex=rule['value-index'], Operation=rule['operation'],
                                         TransformValueMatchPattern=rule['transform-value-match-pattern'], TransformValueReplacementPattern=rule['transform-value-replacement-pattern'],
                                         RetentionDefinitions=rule['retention-definitions'], AdditionalConditions=rule['additional-conditions'],
                                         Groups=rule['groups'])
                elif rule.__class__.__name__ == 'PolicyRule':
                    ruleObj = rule
                    print("1")
                    if hasattr(rule, 'AdditionalConditions'):
                        print(rule.AdditionalConditions.DiscriminatorIndex)
                        print(rule.AdditionalConditions.DiscriminatorValue)
                    print("2")
                    ruleDict = rule.dumpToJson()

                if not ruleDict is None:
                    ruleDicts.append(ruleDict)

                if not ruleObj is None:
                    ruleObjs.append(ruleObj)

        body['rules'] = ruleDicts

        predicateDicts = []
        predicateObjs = []
        for predicate in MatchCriteria:
            if not predicate is None:
                predicateDict = None
                predicateObj = None
                if type(predicate).__name__ == 'dict':
                    predicate = validatePredicateEmptyIndices(predicate)
                    predicateDict = predicate
                    predicateObj = PolicyPredicate(PredicateType=predicate['type'], Name=predicate['name'],
                                                   Operation=predicate['operation'], Field=predicate['field'],
                                                   NumValue=predicate['num-value'],
                                                   HandleUnknownValues=predicate['handle-unknown-values'], Within=predicate['within'],
                                                   Times=predicate['times'], Context=predicate['context'], Tag=predicate['tag'],
                                                   SearchMode=predicate['search-mode'], SearchNumericValues=predicate['search-numeric-values'],
                                                   Values=predicate['values'], GenericGroups=predicate['generic-groups'],
                                                   SqlGroups=predicate['sql-groups'])
                elif predicate.__class__.__name__ == 'PolicyPredicate':
                    predicateObj = predicate
                    predicateDict = predicate.dumpToJson()

                if not predicateDict is None:
                    predicateDicts.append(predicateDict)

                if not predicateObj is None:
                    predicateObjs.append(predicateObj)

        body['match-criteria'] = predicateDicts

        # print(json.dumps(body))

        connection._mx_api('POST', '/conf/dataEnrichmentPolicies/%s' % slash(Name), data=json.dumps(body))
        return DataEnrichmentPolicy(connection=connection, Name=Name, ApplyTo=applyToObjs, Rules=ruleObjs, MatchCriteria=MatchCriteria)


    @staticmethod
    def _update_data_enrichment_policy(connection, Name=None, Rules=[], MatchCriteria=[], ApplyTo=[]):
        raise MxException("Data Enrichment Update API currently not supported")

    @staticmethod
    def _delete_data_enrichment_policy(connection, Name=None):
        raise MxException("Data Enrichment Delete API currently not supported")

    @staticmethod
    def validateRuleEmptyIndices(rule):
        if not type(rule).__name__ == 'dict':
            return rule

        if not 'type' in rule:
            rule['type'] = None
        if not 'order' in rule:
            rule['order'] = None
        if not 'target-field-name' in rule:
            rule['target-field-name'] = None
        if not 'target-field' in rule:
            rule['target-field'] = None
        if not 'enabled' in rule:
            rule['enabled'] = None
        if not 'extraction-method' in rule:
            rule['extraction-method'] = None
        if not 'query' in rule:
            rule['query'] = None
        if not 'value-index' in rule:
            rule['value-index'] = None
        if not 'operation' in rule:
            rule['operation'] = None
        if not 'transform-value-replacement-pattern' in rule:
            rule['transform-value-replacement-pattern'] = None
        if not 'transform-value-match-pattern' in rule:
            rule['transform-value-match-pattern'] = None
        if not 'retention-definitions' in rule:
            rule['retention-definitions'] = None
        if not 'additional-conditions' in rule:
            rule['additional-conditions'] = None
        if not 'groups' in rule:
            rule['groups'] = None

        return rule

    @staticmethod
    def validatePredicateEmptyIndices(predicate):
        if not type(predicate).__name__ == 'dict':
            return predicate

        if not 'type' in predicate:
            predicate['type'] = None
        if not 'name' in predicate:
            predicate['name'] = None
        if not 'operation' in predicate:
            predicate['operation'] = None
        if not 'field' in predicate:
            predicate['field'] = None
        if not 'num-value' in predicate:
            predicate['num-value'] = None
        if not 'handle-unknown-values' in predicate:
            predicate['handle-unknown-values'] = None
        if not 'within' in predicate:
            predicate['within'] = None
        if not 'times' in predicate:
            predicate['times'] = None
        if not 'context' in predicate:
            predicate['context'] = None
        if not 'tag' in predicate:
            predicate['tag'] = None
        if not 'search-mode' in predicate:
            predicate['search-mode'] = None
        if not 'search-numeric-values' in predicate:
            predicate['search-numeric-values'] = None
        if not 'values' in predicate:
            predicate['values'] = None
        if not 'generic-groups' in predicate:
            predicate['generic-groups'] = None
        if not 'sql-groups' in predicate:
            predicate['sql-groups'] = None

        return predicate