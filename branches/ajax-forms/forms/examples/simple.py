import forms
from forms.examples import main

class SimpleFormPage(main.FormExamplePage):
    
    title = 'Simple Form'
    description = 'Probably the simplest form possible.'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('aString', forms.String())
        form.addAction(self.submitted)
        return form

    def submitted(self, ctx, form, data):
        print form, data
