import forms

title = 'Form Types'
description = 'Example of using different typed fields.'

def makeForm(ctx):
    form = forms.Form()
    form.addField('aString', forms.String())
    form.addField('aInteger', forms.Integer())
    form.addField('aFloat', forms.Float())
    form.addField('aBoolean', forms.Boolean())
    form.addField('aDate', forms.Date())
    form.addField('aTime', forms.Time())
    form.addAction(formSubmitted)
    return form

def formSubmitted(ctx, form, data):
    print data

