import forms

title = 'File Upload'
description = 'Uploading a file'

def makeForm(ctx):
    form = forms.Form()
    form.addField('file', forms.File())
    form.addAction(formSubmitted)
    return form

def formSubmitted(ctx, form, data):
    print form, data

