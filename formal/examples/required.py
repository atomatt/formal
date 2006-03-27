import forms
from forms.examples import main

class RequiredFormPage(main.FormExamplePage):

    title = 'Required Fields'
    description = 'Demonstration of required fields'

    def form_example(self, ctx):
        form = forms.Form()
        form.addField('name', forms.String(required=True))
        form.addField('age', forms.Integer())
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print data
