
from zope.interface import implements
from iaforms import IEvent, IEventSource

class EventSource(object):
    implements(IEventSource)

    events = {}

    def __init__(self, events=None):
        if events is not None:
            self.events = events

    def addEvents(self, tag, ctx):
        eventd = dict([(x.event, x.render(ctx)) for x in self.events])
        tag(**eventd)

class CallRemote:
    implements(IEvent)

    def __init__(self, event, method, *args):
        self.event = event
        self.method = method
        self.args = args

    def render(self, ctx):
        return "server.callRemote('%s')" % self.method
