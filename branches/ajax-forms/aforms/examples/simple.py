
import pkg_resources
pkg_resources.require("forms")

from twisted.application import service
from twisted.application import internet

from nevow import rend
from nevow import athena
from nevow import loaders
from nevow import appserver
from nevow import url

import forms
import aforms

things = [
    ('foo', 'Foo'),
    ('bar', 'Bar'),
    ('baz', 'Baz'),
]

class Page(forms.ResourceMixin, athena.LivePage):
    docFactory = loaders.xmlfile("aforms/examples/simple.html")

    def form_example(self, ctx):
        form = aforms.Form()
        wf = forms.widgetFactory(
            aforms.TextArea,
            events=(
                aforms.CallRemote('onkeyup', 'keypressed'),
                aforms.CallRemote('onblur', 'blur', 23),
            )
        )
        form.addField('aString', forms.String(), wf)
        form.addAsyncAction(aforms.CallRemote('onclick', 'async_submitted'))
        return form

    def submitted(self, ctx, form, data):
        print form, data

class Root(rend.Page):
    def child_(self, ctx):
        return url.URL.fromString('/app')

    def child_app(self, ctx):
        page = Page((), None)
        return page

root = Root()
application = service.Application("test")
i = internet.TCPServer(9898, appserver.NevowSite(root,  logPath="/dev/null"))
i.setServiceParent(application)

