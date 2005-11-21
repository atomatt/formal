import pkg_resources
from twisted.python import reflect
from nevow import appserver, loaders, rend, static, tags as T, url
import forms

DOCTYPE = T.xml('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
CHARSET = T.xml('<meta http-equiv="content-type" content="text/html; charset=utf-8" />')

examples = [
    'forms.examples.simple.SimpleFormPage',
    'forms.examples.types.TypesFormPage',
    'forms.examples.required.RequiredFormPage',
    'forms.examples.missing.MissingFormPage',
    'forms.examples.prepopulate.PrepopulateFormPage',
    'forms.examples.fileupload.FileUploadFormPage',
    'forms.examples.smartupload.SmartUploadFormPage',
    'forms.examples.selections.SelectionFormPage',
    'forms.examples.dates.DatesFormPage',
    'forms.examples.actionbuttons.ActionButtonsPage',
    ]

def makeSite(application):
    root = RootPage()
    site = appserver.NevowSite(root, logPath='web.log')
    return site

class RootPage(rend.Page):
    """
    Main page that lists the examples and makes the example page a child
    resource.
    """

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
            cls = reflect.namedAny(name)
            yield T.div(class_='example')[
                T.h1[T.a(href=url.here.child(name))[cls.title]],
                T.p[cls.description],
                ]

    def childFactory(self, ctx, name):
        if name in examples:
            cls = reflect.namedAny(name)
            return cls()


class FormExamplePage(forms.ResourceMixin, rend.Page):
    """
    A base page for the actual examples. The page renders something sensible,
    including the title example and description. It also include the "example"
    form in an appropriate place.
    
    Each example page is expected to provide the title and description
    attributes as well as a form_example method that builds and returns a
    forms.Form instance.
    """
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
        return self.title

    def data_description(self, ctx, data):
        return self.description


# Add child_ attributes
examples_css = pkg_resources.resource_filename('forms.examples', 'examples.css')
setattr(RootPage, 'child_examples.css', static.File(examples_css))
setattr(RootPage, 'child_forms.css', forms.defaultCSS)
