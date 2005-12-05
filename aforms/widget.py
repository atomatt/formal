
import forms
from nevow import tags as T

from event import EventSource

class TextArea(forms.TextArea, EventSource):

    def __init__(self, original, cols=None, rows=None, events=None):
        forms.TextArea.__init__(self, original, cols, rows)
        EventSource.__init__(self, events)

    def _renderTag(self, ctx, key, value, readonly):
        tag=T.textarea(name=key,
                       id=forms.util.keytocssid(ctx.key),
                       cols=self.cols,
                       rows=self.rows,
                       )[value or '']
        self.addEvents(tag, ctx)
        if readonly:
            tag(class_='readonly', readonly='readonly')
        return tag
