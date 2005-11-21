from datetime import date
import forms
from forms.examples import main

class MissingFormPage(main.FormExamplePage):

    title = 'Missing Values'
    description = 'Providing default values when missing'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('aString', forms.String(missing='<nothing>'))
        form.addField('aDate', forms.Date(missing=date(2005, 8, 1)))
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print data
