from nevow import url
import forms

title = 'Extra Button'
description = 'Example of adding an extra, non-validating button'

def makeForm(ctx):
    form = forms.Form()
    form.addField('aString', forms.String(required=True))
    form.addAction(formSubmitted)
    form.addAction(redirect, 'back', validate=False)
    return form

def formSubmitted(ctx, form, data):
    print form, data

def redirect(ctx, form, data):
    return url.rootaccessor(ctx)
