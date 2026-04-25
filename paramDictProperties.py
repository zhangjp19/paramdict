from .localization import l10n
_ = l10n.gettext

from typing import get_type_hints, Callable, List

from enum import Enum

from .paramDictHandler import baseParamDict

from .colorOutput import outGreen, outRed, outYellow

__all__ = ['pSimple', 'pSimpleOpt', 'pStrict', 'pStrictOpt',
           'UNSET', 'SET',
           'pList', 'pListOpt',
           'pPd', 'pPdOpt', 'pPdList', 'pPdListOpt',
           'pEnm', 'pEnmOpt', 'pEnmList', 'pEnmListOpt']

class ValueStatus(Enum):
    UNSET = 0
    SET = 1

UNSET = ValueStatus.UNSET
'Specific representation of an unset value.'

SET = ValueStatus.SET
'Specific representation of a value that has been set.'

class pdprop(object):

    def __set_name__(self, owner, name):
        self._status_name = '_status_' + name

    def __init__(self, func):
        self.fget = func

class pSimple(pdprop):
    'Simple property. No type checking. Must be set before getting.'

    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        return value
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        instance._cont[self.fget.__name__] = aType(value)

class pSimpleOpt(pdprop):
    'Simple property. No type checking. Optional.'
    def __get__(self, instance:baseParamDict, owner):
        return instance._cont.get(self.fget.__name__, UNSET)
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        instance._cont[self.fget.__name__] = aType(value)
    
    def __delete__(self, instance:baseParamDict):
        instance._cont.pop(self.fget.__name__, None)

# def pSimple(opt=False):
#     if opt:
#         return _pSimpleOpt
#     else:
#         return _pSimple

class pStrict(pdprop):
    'Strict property. Type checking enforced. Must be set before getting.'

    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        return value
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value

class pStrictOpt(pdprop):
    'Strict property. Type checking enforced. Optional.'
    def __get__(self, instance:baseParamDict, owner):
        return instance._cont.get(self.fget.__name__, UNSET)
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value
    
    def __delete__(self, instance:baseParamDict):
        instance._cont.pop(self.fget.__name__, None)

class pList(pdprop):
    'List property. Type checking enforced. Must be set before getting.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        return value
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        if not isinstance(value, list):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = value

class pListOpt(pdprop):
    'List property. Type checking enforced. Optional.'
    def __get__(self, instance:baseParamDict, owner):
        return instance._cont.get(self.fget.__name__, UNSET)
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        if not isinstance(value, list):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = value
    
    def __delete__(self, instance:baseParamDict):
        instance._cont.pop(self.fget.__name__, None)

class pPd(pdprop):
    'ParamDict property. Type checking enforced. Must be set before getting.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return']
        return aType(source=instance._cont[self.fget.__name__])
    
    def __set__(self, instance:baseParamDict, value:baseParamDict):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.content

class pPdOpt(pdprop):
    'ParamDict property. Type checking enforced. Optional.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            return UNSET
        aType:type = get_type_hints(self.fget)['return']
        return aType(source=value)
    
    def __set__(self, instance:baseParamDict, value:baseParamDict):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.content
    
    def __delete__(self, instance:baseParamDict):
        instance._cont.pop(self.fget.__name__, None)

class pPdList(pdprop):
    'ParamDict List property. Type checking enforced. Must be set before getting.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(source=item) for item in value]
    
    def __set__(self, instance:baseParamDict, value:'list[baseParamDict]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.content for item in value]

class pPdListOpt(pdprop):
    'ParamDict List property. Type checking enforced. Optional.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            return UNSET
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(source=item) for item in value]
    
    def __set__(self, instance:baseParamDict, value:'list[baseParamDict]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.content for item in value]
    
    def __delete__(self, instance:baseParamDict):
        instance._cont.pop(self.fget.__name__, None)

class pEnm(pdprop):
    'Enum property. Type checking enforced. Must be set before getting.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return']
        return aType(value)
    
    def __set__(self, instance:baseParamDict, value:Enum):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.value

class pEnmOpt(pdprop):
    'Enum property. Type checking enforced. Optional.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            return UNSET
        aType:type = get_type_hints(self.fget)['return']
        return aType(value)
    
    def __set__(self, instance:baseParamDict, value:Enum):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.value
    
    def __delete__(self, instance:baseParamDict):
        instance._cont.pop(self.fget.__name__, None)

class pEnmList(pdprop):
    'Enum List property. Type checking enforced. Must be set before getting.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(item) for item in value]
    
    def __set__(self, instance:baseParamDict, value:'list[Enum]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.value for item in value]

class pEnmListOpt(pdprop):
    'Enum List property. Type checking enforced. Optional.'
    def __get__(self, instance:baseParamDict, owner):
        value = instance._cont.get(self.fget.__name__, UNSET)
        if value is UNSET:
            return UNSET
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(item) for item in value]
    
    def __set__(self, instance:baseParamDict, value:'list[Enum]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.value for item in value]
    
    def __delete__(self, instance:baseParamDict):
        instance._cont.pop(self.fget.__name__, None)
