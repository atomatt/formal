import pkg_resources
from twisted.python import reflect
from nevow import appserver, loaders, rend, static, tags as T, url
import forms

DOCTYPE = T.xml('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
CHARSET = T.xml('<meta http-equiv="content-type" content="text/html; charset=utf-8" />')

examples = [
    'forms.examples.simple',
    'forms.examples.types',
    'forms.examples.required',
    'forms.examples.missing',
    'forms.examples.prepopulate',
    'forms.examples.fileupload',
    'forms.examples.smartupload',
    'forms.examples.selections',
    'forms.examples.dates',
    'forms.examples.extrabutton',
    ]

def makeSite(application):
    root = RootPage()
    site = appserver.NevowSite(root, logPath='web.log')
    return site

class RootPage(rend.Page):

    docFactory = loaders.stan(
        T.invisible[
            DOCTYPE,
            T.html[
                T.head[
                    CHARSET,
                    T.title['Forms Examples'],
                    T.link(rel='stylesheet', type='text/css', href=url.root.child('examples.css')),
                    ],
                T.body[
                    T.directive('examples'),
                    ],
                ],
            ],
        )

    def render_examples(self, ctx, data):
        for name in examples:
            module = reflect.namedAny(name)
            yield T.div(class_='example')[
                T.h1[T.a(href=url.here.child(name))[module.title]],
                T.p[module.description],
                ]

    def childFactory(self, ctx, name):
        if name in examples:
            return FormExamplePage(reflect.namedAny(name))



class FormPage(rend.Page):
    """
    Base class for pages that contain a Form.

    XXX This really, really needs to turn into a ComponentPage that iterates
    a bunch of component behaviours looking for something that succeeded.

    The components probably needs to be per-interface, i.e IResource for
    locateChild/renderHTTP, IRenderer for render_, etc.
    """

    def __init__(self, *a, **k):
        rend.Page.__init__(self, *a, **k)
        self._formsComponent = forms.ResourceComponent(parent=self)

    def locateChild(self, ctx, segments):
        def gotResult(result):
            if result is not appserver.NotFound:
                return result
            return rend.Page.locateChild(self, ctx, segments)
        d = defer.maybeDeferred(self._formsComponent.locateChild, ctx, segments)
        d.addCallback(gotResult)
        return d

    def renderHTTP(self, ctx):
        def gotResult(result):
            if result is not None:
                return result
            return rend.Page.renderHTTP(self, ctx)
        d = defer.maybeDeferred(self._formsComponent.renderHTTP, ctx)
        d.addCallback(gotResult)
        return d

    def render_form(self, name):
        return self._formsComponent.render_form(name)

    def formFactory(self, ctx, name):
        # Find the factory method
        factory = getattr(self, 'form_%s'%name, None)
        if factory is not None:
            return factory(ctx)
        # Try the super class
        s = super(ResourceMixin, self)
        if hasattr(s,'formFactory'):
            return s.formFactory(ctx, name)


class FormExamplePage(forms.ResourceMixin, rend.Page):
#class FormExamplePage(FormPage):
    docFactory = loaders.stan(
        T.invisible[
            DOCTYPE,
            T.html[
                T.head[
                    CHARSET,
                    T.title(data=T.directive('title'), render=rend.data),
                    T.link(rel='stylesheet', type='text/css', href=url.root.child('examples.css')),
                    T.link(rel='stylesheet', type='text/css', href=url.root.child('forms.css')),
                    ],
                T.body[
                    T.h1(data=T.directive('title'), render=rend.data),
                    T.p(data=T.directive('description'), render=rend.data),
                    T.directive('form example'),
                    ],
                ],
            ],
        )

    def data_title(self, ctx, data):
        return self.original.title

    def data_description(self, ctx, data):
        return self.original.description

    def form_example(self, ctx):
        return self.original.makeForm(ctx)


# Add child_ attributes
examples_css = pkg_resources.resource_filename('forms.examples', 'examples.css')
setattr(RootPage, 'child_examples.css', static.File(examples_css))
setattr(RootPage, 'child_forms.css', forms.defaultCSS)

