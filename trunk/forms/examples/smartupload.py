import forms

title = 'Smart File Upload'
description = 'Smart uploading of files where the file is "carried across" when the validation fails'

def makeForm(ctx):
    form = forms.Form()
    form.addField('required', forms.String(required=True))
    form.addField('file', forms.File(), forms.FileUploadWidget)
    form.addAction(formSubmitted)
    return form

def formSubmitted(ctx, form, data):
    print form, data
    print '*****', len(data['file'][1].read())
    
