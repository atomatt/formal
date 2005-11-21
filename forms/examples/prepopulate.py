from datetime import datetime
import forms
from forms.examples import main

class PrepopulateFormPage(main.FormExamplePage):

    title = 'Prepopulate'
    description = 'Example of prepopulating form fields'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('aString', forms.String())
        form.addField('aTime', forms.Time())
        form.addAction(self.submitted)
        form.data = {
            'aTime': datetime.utcnow().time(),
            }
        return form
    
    def submitted(self, ctx, form, data):
        print data

