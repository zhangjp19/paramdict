def readonly(varname:str, vartype:str=None):
    if vartype is None:
        s = """
    @property
    def {n}(self):
        return self._cont['{n}']
""".format(n=varname)
    else:
        s = """
    @property
    def {n}(self) -> {t}:
        return self._cont['{n}'].astype('{t}')
""".format(n=varname, t=vartype)
    return s

def rwsimple(varname:str, vartype:str=None):
    if vartype is None:
        s = """
    @property
    def {n}(self):
        return self._cont['{n}']
    @{n}.setter
    def {n}(self, val):
        self._cont['{n}'] = val
""".format(n=varname)
    else:
        s = """
    @property
    def {n}(self) -> {t}:
        return self._cont['{n}']
    @{n}.setter
    def {n}(self, val):
        self._cont['{n}'] = {t}(val)
""".format(n=varname, t=vartype)
    return s
