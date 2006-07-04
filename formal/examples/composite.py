from zope.interface import implements
from twisted.python.components import registerAdapter
from nevow import inevow, tags as T
import formal, formal.iformal, formal.types, formal.widget, formal.util
from formal.examples import main



#####
# TODO:
#
#  * composition labels, and position (?)
#  * composition widgets
#  * composition errors (?)
#  * composition description (?)
#  * Validate XHTML
#



class Composite(formal.types.Type):

    def __init__(self, composition, *a, **k):
        super(Composite, self).__init__(*a, **k)
        self.composition = composition


    def validate(self, value):

        # If nothing has been entered then we'll have a sequence of None
        # instances, in which case my value if None (not a sequence). If there
        # is anything other than None in the sequence then pass validation on to
        # the composite types.
        if not filter(None, value):
            value = None
        else:
            value = dict([
                    (name, type.validate(value))
                    for (name, type), value in zip(self.composition, value)])

        # Allow normal validation to run on the new value
        return super(Composite, self).validate(value)



class CompositeWidget(object):
    implements(formal.iformal.IWidget)


    labels = None
    widgetFactories = None


    def __init__(self, composite, labels=None, widgetFactories=None):
        self.composite = composite
        if labels is not None:
            self.labels = labels
        if widgetFactories is not None:
            self.widgetFactories = widgetFactories


    def render(self, ctx, key, args, errors):
        for name, type in self.composite.composition:
            childKey = '.'.join([key, name])
            yield T.div(class_=name)[
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



registerAdapter(CompositeWidget, Composite, formal.iformal.IWidget)



class CompositeFormPage(main.FormExamplePage):
    
    title = 'Composite fields'
    description = 'Form containing composite fields'
    
    def form_example(self, ctx):

        # Create the form
        form = formal.Form()

        # Add a required name where the family name is required but the first
        # name is optional.
        form.add(formal.Field('name', Composite([
            ('family', formal.String(required=True)),
            ('first', formal.String())],
            required=True)))

        # Add an optional temperature field where, once entered, both values
        # must be entered.
        form.add(formal.Field('temperature', Composite([
            ('temperature', formal.Integer(required=True)),
            ('units', formal.String(required=True))])))

        # Add a required height field where both values are also required.
        form.add(formal.Field('height', Composite([
            ('feet', formal.Integer(required=True)),
            ('inches', formal.Integer(required=True))],
            required=True)))

        # Add the submit action
        form.addAction(self.submitted)

        return form

    def submitted(self, ctx, form, data):
        print form, data
