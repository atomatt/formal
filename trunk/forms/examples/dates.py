import forms
from forms.examples import main

class DatesFormPage(main.FormExamplePage):

    title = 'Dates'
    description = 'Date entry examples'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('isoFormat', forms.Date(), forms.TextInput)
        form.addField('monthFirst', forms.Date(), forms.DatePartsInput)
        form.addField('dayFirst', forms.Date(), forms.widgetFactory(forms.DatePartsInput, dayFirst=True))
        form.addField('monthAndYear', forms.Date(), forms.MMYYDatePartsInput)
        form.addField('twoCharYear', forms.Date(), forms.widgetFactory(forms.DatePartsInput, twoCharCutoffYear=70))
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print form, data
