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
SET = ValueStatus.SET

class pdprop(object):

    def __set_name__(self, owner, name):
        self._status_name = '_status_' + name

    def __init__(self, func):
        self.fget = func

class pSimple(pdprop):

    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        return instance._cont[self.fget.__name__]
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        instance._cont[self.fget.__name__] = aType(value)
        setattr(instance, self._status_name, 1)

class pSimpleOpt(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return UNSET
        return instance._cont[self.fget.__name__]
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        instance._cont[self.fget.__name__] = aType(value)
        setattr(instance, self._status_name, 1)
    
    def __delete__(self, instance:baseParamDict):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return
        instance._cont.pop(self.fget.__name__, None)
        setattr(instance, self._status_name, 0)

# def pSimple(opt=False):
#     if opt:
#         return _pSimpleOpt
#     else:
#         return _pSimple

class pStrict(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        return instance._cont[self.fget.__name__]
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value
        setattr(instance, self._status_name, 1)

class pStrictOpt(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return UNSET
        return instance._cont[self.fget.__name__]
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value
        setattr(instance, self._status_name, 1)
    
    def __delete__(self, instance:baseParamDict):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return
        instance._cont.pop(self.fget.__name__, None)
        setattr(instance, self._status_name, 0)

# def pStrict(opt=False):
#     if opt:
#         return _pStrictOpt
#     else:
#         return _pStrict

class pList(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        return instance._cont[self.fget.__name__]
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        if not isinstance(value, list):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = value
        setattr(instance, self._status_name, 1)

class pListOpt(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return UNSET
        return instance._cont[self.fget.__name__]
    
    def __set__(self, instance:baseParamDict, value):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        if not isinstance(value, list):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = value
        setattr(instance, self._status_name, 1)
    
    def __delete__(self, instance:baseParamDict):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return
        instance._cont.pop(self.fget.__name__, None)
        setattr(instance, self._status_name, 0)

class pPd(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return']
        return aType(source=instance._cont[self.fget.__name__])
    
    def __set__(self, instance:baseParamDict, value:baseParamDict):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.content
        setattr(instance, self._status_name, 1)

class pPdOpt(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return UNSET
        aType:type = get_type_hints(self.fget)['return']
        return aType(source=instance._cont[self.fget.__name__])
    
    def __set__(self, instance:baseParamDict, value:baseParamDict):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.content
        setattr(instance, self._status_name, 1)
    
    def __delete__(self, instance:baseParamDict):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return
        instance._cont.pop(self.fget.__name__, None)
        setattr(instance, self._status_name, 0)

class pPdList(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(source=item) for item in instance._cont[self.fget.__name__]]
    
    def __set__(self, instance:baseParamDict, value:'list[baseParamDict]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.content for item in value]
        setattr(instance, self._status_name, 1)

class pPdListOpt(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return UNSET
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(source=item) for item in instance._cont[self.fget.__name__]]
    
    def __set__(self, instance:baseParamDict, value:'list[baseParamDict]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.content for item in value]
        setattr(instance, self._status_name, 1)
    
    def __delete__(self, instance:baseParamDict):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return
        instance._cont.pop(self.fget.__name__, None)
        setattr(instance, self._status_name, 0)

class pEnm(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return']
        return aType(instance._cont[self.fget.__name__])
    
    def __set__(self, instance:baseParamDict, value:Enum):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.value
        setattr(instance, self._status_name, 1)

class pEnmOpt(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return UNSET
        aType:type = get_type_hints(self.fget)['return']
        return aType(instance._cont[self.fget.__name__])
    
    def __set__(self, instance:baseParamDict, value:Enum):
        aType:type = get_type_hints(self.fget)['return']
        if not isinstance(value, aType):
            raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(aType)))
        instance._cont[self.fget.__name__] = value.value
        setattr(instance, self._status_name, 1)
    
    def __delete__(self, instance:baseParamDict):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return
        instance._cont.pop(self.fget.__name__, None)
        setattr(instance, self._status_name, 0)

class pEnmList(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            raise AttributeError(_('Property %s not set.') % outYellow('\''+self.fget.__name__+'\''))
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(item) for item in instance._cont[self.fget.__name__]]
    
    def __set__(self, instance:baseParamDict, value:'list[Enum]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.value for item in value]
        setattr(instance, self._status_name, 1)

class pEnmListOpt(pdprop):
    def __get__(self, instance:baseParamDict, owner):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return UNSET
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        return [aType(item) for item in instance._cont[self.fget.__name__]]
    
    def __set__(self, instance:baseParamDict, value:'list[Enum]'):
        aType:type = get_type_hints(self.fget)['return'].__args__[0]
        for item in value:
            if not isinstance(item, aType):
                raise TypeError(_('Property %s must be of type %s.') % (outYellow('\''+self.fget.__name__+'\''), outGreen(List[aType])))
        instance._cont[self.fget.__name__] = [item.value for item in value]
        setattr(instance, self._status_name, 1)
    
    def __delete__(self, instance:baseParamDict):
        status = getattr(instance, self._status_name, 0)
        if status == 0:
            return
        instance._cont.pop(self.fget.__name__, None)
        setattr(instance, self._status_name, 0)
