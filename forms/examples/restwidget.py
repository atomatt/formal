import forms
from forms.examples import main
from docutils.writers.html4css1 import Writer, HTMLTranslator
from docutils import nodes


class CustomisedHTMLTranslator(HTMLTranslator):
    def visit_newdirective_node(self, node):
        self.body.append('<div>Some HTML with a %s parameter</div>\n'%(node.attributes['parameter'],))

    def depart_newdirective_node(self, node):
        pass

class newdirective_node(nodes.General, nodes.Inline, nodes.TextElement):
    pass

def newdirective(name, arguments, options, content, lineno,
                 content_offset, block_text, state, state_machine):
    return [newdirective_node('', parameter=arguments[0])]

newdirective.arguments = (1, 0, 0)
newdirective.options = None

from docutils.parsers.rst import directives
directives.register_directive('newdirective', newdirective)


class ReSTWidgetFormPage(main.FormExamplePage):
    
    title = 'ReST widget'
    description = 'The ReST widget captures ReST and previews as HTML.'
    
    def form_example(self, ctx):
        w = Writer()
        w.translator_class = CustomisedHTMLTranslator

        form = forms.Form()
        form.addField('restString', forms.String(required=True), forms.widgetFactory(forms.ReSTTextArea, restWriter=w))
        form.addAction(self.submitted)

        return form

    def submitted(self, ctx, form, data):
        print form, data
