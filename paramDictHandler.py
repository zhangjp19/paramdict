from .localization import l10n
_ = l10n.gettext

from abc import ABC, abstractmethod

__all__ = ['baseParamDict']

class baseParamDict(ABC):
    '''
    Base class for paramdicts.

    :param id: The ID of the paramdict. Must be a string.
    :param source: The source dict to initialize the paramdict from. If None, a new paramdict will be created.

    :type id: str
    :type source: dict or None
    '''
    def __init__(self, id:str='', source=None):
        super().__init__()
        if type(id) is not str:
            raise TypeError(_('Paramdict ID must be a string!'))
        if source is None:
            self._cont = {'class': self._setcls(), 'id': id}
            self._id = self._cont['id']
            self._cla = self._cont['class']
            self._pdinit()
        else:
            self._cont = source
            if self._cont['class'] != self._setcls():
                raise TypeError(_('Paramdict Class mismatch!'))
            self._id = self._cont['id']
            self._cla = self._cont['class']
        self._check()
    @abstractmethod
    def _setcls(self):
        pass
    @abstractmethod
    def _pdinit(self):
        pass
    @abstractmethod
    def _check(self):
        return True

    @property
    def id(self):
        'Returns the ID of the paramdict.'
        return self._id
    @property
    def cla(self):
        'Returns the class of the paramdict.'
        return self._cla
    @property
    def content(self):
        'Returns the content dict of the paramdict. All contents of this dict can be changed, including class and id.'
        return self._cont
