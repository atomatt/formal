from nevow import url
import forms

title = 'Action Button'
description = 'Example of non-validating button, buttons with non-default labels, etc'

def makeForm(ctx):
    form = forms.Form()
    form.addField('aString', forms.String(required=True))
    form.addAction(formSubmitted, label="Click, click, clickety-click!")
    form.addAction(redirect, 'back', validate=False)
    return form

def formSubmitted(ctx, form, data):
    print form, data

def redirect(ctx, form, data):
    return url.rootaccessor(ctx)
