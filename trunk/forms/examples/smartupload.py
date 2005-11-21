import forms
from forms.examples import main

class SmartUploadFormPage(main.FormExamplePage):

    title = 'Smart File Upload'
    description = 'Smart uploading of files where the file is "carried across" when the validation fails'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('required', forms.String(required=True))
        form.addField('file', forms.File(), forms.FileUploadWidget)
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print form, data
