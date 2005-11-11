from datetime import date
import forms

title = 'Missing Values'
description = 'Providing default values when missing'

def makeForm(ctx):
    form = forms.Form()
    form.addField('aString', forms.String(missing='<nothing>'))
    form.addField('aDate', forms.Date(missing=date(2005, 8, 1)))
    form.addAction(formSubmitted)
    return form

def formSubmitted(ctx, form, data):
    print data
