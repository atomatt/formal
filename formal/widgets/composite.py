__all__ = ['CompositeWidget']


from zope.interface import implements
from nevow import tags as T
import formal.iformal, formal.util



#####
# TODO:
#  * composition labels, and position (?)
#  * composition widgets
#  * composition errors (?)
#  * composition description (?)
#  * Validate XHTML



class CompositeWidget(object):
    implements(formal.iformal.IWidget)


    def __init__(self, composite):
        self.composite = composite


    def render(self, ctx, key, args, errors):
        return self._render(ctx, key, args, errors, False)


    def renderImmutable(self, ctx, key, args, errors):
        return self._render(ctx, key, args, errors, True)


    def processInput(self, ctx, key, args):
        value = []
        for name, type in self.composite.composition:
            childKey = '.'.join([key, name])
            value.append(formal.iformal.IWidget(type).processInput(ctx,
                childKey, args))
        return tuple(value)


    def _render(self, ctx, key, args, errors, immutable):

        if not errors:
            value = args.get(key) or {}
        else:
            value = None

        for name, type in self.composite.composition:

            childKey = '.'.join([key, name])
            if value is not None:
                args = {childKey: value.get(name)}

            widget = formal.iformal.IWidget(type)
            if immutable:
                widgetRenderer = widget.renderImmutable
            else:
                widgetRenderer = widget.render

            yield T.div(class_=('composite-component', ' ', name))[
                T.label(for_=formal.util.render_cssid(childKey))[
                    formal.util.titleFromName(name)
                    ],
                widgetRenderer(ctx, childKey, args, errors)
                ]
