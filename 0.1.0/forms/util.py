from forms import iforms
from zope.interface import implements


def titleFromName(name):

    def _():

        it = iter(name)
        last = None

        while 1:
            ch = it.next()
            if ch == '_':
                if last != '_':
                    yield ' '
            elif last in (None,'_'):
                yield ch.upper()
            elif ch.isupper() and not last.isupper():
                yield ' '
                yield ch.upper()
            else:
                yield ch
            last = ch

    return ''.join(_())

    
def keytocssid(key):
    return '-'.join(key.split('.'))
    
        
class SequenceKeyLabelAdapter(object):
    implements( iforms.IKey, iforms.ILabel )
    
    def __init__(self, original):
        self.original = original
        
    def key(self):
        return self.original[0]
        
    def label(self):
        return self.original[1]
        
