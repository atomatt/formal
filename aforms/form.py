
from zope.interface import Interface, implements
from twisted.python.components import Adapter

from nevow.compy import registerAdapter
from nevow import tags as T
from nevow import inevow

import forms

class AsyncAction(forms.form.Action):
    pass

class IActionRenderer(Interface): pass

class ActionRenderer(Adapter):

    def render(self, ctx):
        return T.input(type='submit', 
                       id='%s-action-%s' % (forms.util.keytocssid(ctx.key), 
                                            self.original.name), 
                       name=self.original.name, 
                       value=self.original.label)

registerAdapter(ActionRenderer, forms.form.Action, IActionRenderer)

class AsyncActionRenderer(Adapter):

    def render(self, ctx):
        return T.input(type='button',
                       id='%s-action-%s' % (forms.util.keytocssid(ctx.key), 
                                            self.original.name), 
                       onclick=self.original.callback.render(ctx),
                       name=self.original.name, 
                       value=self.original.label)

registerAdapter(AsyncActionRenderer, AsyncAction, IActionRenderer)

class Form(forms.Form):

    def addAsyncAction(self, callback, name='submit', validate=True, label=None):
        if self.actions is None:
            self.actions = []
        if name in [action.name for actions in self.actions]:
            raise ValueError('Action with name %r already exists.' % name)
        self.actions.append(AsyncAction(callback, name, validate, label))

class FormRenderer(forms.form.FormRenderer):
    def _renderAction(self, ctx, data):
        return IActionRenderer(data).render(ctx)

registerAdapter(FormRenderer, Form, inevow.IRenderer)
