import forms

title = 'ReST widget'
description = 'The ReST widget captures ReST and previews as HTML.'

def makeForm(ctx):
    form = forms.Form()
    form.addField('aString', forms.String(required=True))
    form.addField('restString', forms.String(required=True), widgetFactory=forms.ReSTTextArea)
    form.addAction(formSubmitted)

    return form

def formSubmitted(ctx, form, data):
    print form, data

