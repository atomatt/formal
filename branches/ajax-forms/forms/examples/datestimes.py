import forms
from forms.examples import main

class DatesTimesFormPage(main.FormExamplePage):

    title = 'Dates'
    description = 'Date entry examples'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('isoFormatDate', forms.Date(), forms.TextInput)
        form.addField('monthFirstDate', forms.Date(), forms.DatePartsInput)
        form.addField('dayFirstDate', forms.Date(), forms.widgetFactory(forms.DatePartsInput, dayFirst=True))
        form.addField('monthYearDate', forms.Date(), forms.MMYYDatePartsInput)
        form.addField('twoCharYearDate', forms.Date(), forms.widgetFactory(forms.DatePartsInput, twoCharCutoffYear=70))
        form.addField('time', forms.Time())
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print form, data
