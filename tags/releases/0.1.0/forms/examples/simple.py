import forms

title = 'Simple Form'
description = 'Probably the simplest form possible.'

def makeForm(ctx):
    form = forms.Form()
    form.addField('aString', forms.String())
    form.addAction(formSubmitted)
    return form

def formSubmitted(ctx, form, data):
    print form, data

