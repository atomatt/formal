import forms
from forms.examples import main

class NoFieldsFormPage(main.FormExamplePage):
    
    title = 'Form With no Fields'
    description = 'A form with no fields, just button(s). (Just to prove ' \
            'it works.)'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addAction(self.submitted)
        return form

    def submitted(self, ctx, form, data):
        print form, data

