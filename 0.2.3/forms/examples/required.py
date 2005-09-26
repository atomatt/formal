import forms

title = 'Required Fields'
description = 'Demonstration of required fields'

def makeForm(ctx):
    form = forms.Form()
    form.addField('name', forms.String(required=True))
    form.addField('age', forms.Integer())
    form.addAction(formSubmitted)
    return form

def formSubmitted(ctx, form, data):
    print data
    
