from datetime import datetime
import forms

title = 'Prepopulate'
description = 'Example of prepopulating form fields'

def makeForm(ctx):
    form = forms.Form()
    form.addField('aString', forms.String())
    form.addField('aTime', forms.Time())
    form.addAction(formSubmitted)
    form.data = {
        'aTime': datetime.utcnow().time(),
        }
    return form

def formSubmitted(ctx, form, data):
    print data

