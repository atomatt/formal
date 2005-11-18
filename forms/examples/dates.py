import forms

title = 'Dates'
description = 'Date entry examples'

def makeForm(ctx):
    form = forms.Form()
    form.addField('isoFormat', forms.Date(), forms.TextInput)
    form.addField('monthFirst', forms.Date(), forms.DatePartsInput)
    form.addField('dayFirst', forms.Date(), forms.widgetFactory(forms.DatePartsInput, dayFirst=True))
    form.addField('monthAndYear', forms.Date(), forms.MMYYDatePartsInput)
    form.addField('twoCharYear', forms.Date(), forms.widgetFactory(forms.DatePartsInput, twoCharCutoffYear=70))
    form.addAction(formSubmitted)
    return form

def formSubmitted(ctx, form, data):
    print form, data

