from zope.interface import implements
from nevow import inevow
from forms import iforms


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


class LazyResource(object):
    implements(inevow.IResource)

    def __init__(self, factory):
        self.factory = factory
        self._resource = None

    def locateChild(self, ctx, segments):
        return self.resource().locateChild(ctx, segments)

    def renderHTTP(self, ctx):
        return self.resource().renderHTTP(ctx)

    def resource(self):
        if self._resource is None:
            self._resource = self.factory()
        return self._resource
