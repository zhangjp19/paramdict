import locale
import gettext

__all__ = ['l10n']

current_dir = __file__.rsplit('/', 1)[0]

loc = locale.getlocale()
if loc[0] is None:
    loc = ('en_US', 'UTF-8')
l10n = gettext.translation(loc[0], localedir=f'{current_dir}/locale', languages=[loc[0]], fallback=True)
