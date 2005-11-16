import forms
from docutils.writers.html4css1 import Writer, HTMLTranslator
from docutils import nodes

title = 'ReST widget'
description = 'The ReST widget captures ReST and previews as HTML.'


class CustomisedHTMLTranslator(HTMLTranslator):
    def visit_newdirective_node(self, node):
        self.body.append('<div>Some HTML with a %s parameter</div>\n'%(node.attributes['parameter'],))

    def depart_newdirective_node(self, node):
        pass

def makeForm(ctx):
    w = Writer()
    w.translator_class = CustomisedHTMLTranslator

    form = forms.Form()
    form.addField('aString', forms.String(required=True))
    form.addField('restString', forms.String(required=True), forms.widgetFactory(forms.ReSTTextArea, restWriter=w))
    form.addAction(formSubmitted)

    form.data = dict(restString='Hello World')

    return form

def formSubmitted(ctx, form, data):
    print form, data

class newdirective_node(nodes.General, nodes.Inline, nodes.TextElement):
    pass

def newdirective(name, arguments, options, content, lineno,
                 content_offset, block_text, state, state_machine):
    return [newdirective_node('', parameter=arguments[0])]

newdirective.arguments = (1, 0, 0)
newdirective.options = None

from docutils.parsers.rst import directives
directives.register_directive('newdirective', newdirective)
