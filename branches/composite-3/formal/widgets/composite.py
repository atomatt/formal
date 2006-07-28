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

        if not errors:
            value = args.get(key) or {}
        else:
            value = None

        for name, type in self.composite.composition:
            childKey = '.'.join([key, name])
            if value is not None:
                args = {childKey: value.get(name)}
            yield T.div(class_=('composite-component', ' ', name))[
                T.label(for_=formal.util.render_cssid(childKey))[
                    formal.util.titleFromName(name)
                    ],
                formal.iformal.IWidget(type).render(ctx, childKey, args, errors)
                ]


    def renderImmutable(self, ctx, key, args, errors):
        for name, type in self.composite.composition:
            childKey = '.'.join([key, name])
            yield T.div(class_=name)[
                T.label[formal.util.titleFromName(name)],
                formal.iformal.IWidget(type).renderImmutable(ctx, childKey,
                        args, errors)
                ]


    def processInput(self, ctx, key, args):
        value = []
        for name, type in self.composite.composition:
            childKey = '.'.join([key, name])
            value.append(formal.iformal.IWidget(type).processInput(ctx,
                childKey, args))
        return tuple(value)
