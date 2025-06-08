import json
from pathlib import Path
from abc import ABC, abstractmethod
from copy import copy, deepcopy
from functools import wraps

pdPathRoot = Path('./')

def changePdPathRoot(pathRoot: Path):
    global pdPathRoot
    pdPathRoot = pathRoot

def getAllPdPaths():
    pass

def getPdFile(path: Path):
    with open(pdPathRoot + path, 'r') as jsfile:
        pdfile = json.load(jsfile)
    return pdfile

def savePd(path, pd):
    with open(pdPathRoot + path, 'w') as jsfile:
        json.dump(pd.content, jsfile)

class baseParamDict(ABC):
    def __init__(self, id:str='', source=None):
        super().__init__()
        if type(id) is not str:
            raise TypeError('Paramdict ID must be a string!')
        if source is None:
            self._cont = {'class': self._setcls(), 'id': id}
            self._id = self._cont['id']
            self._cla = self._cont['class']
            self._pdinit()
        else:
            self._cont = source
            if self._cont['class'] != self._setcls():
                raise TypeError('Paramdict Class mismatch!')
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
        return self._id
    @property
    def cla(self):
        return self._cla
    @property
    def content(self):
        return self._cont

