import forms
from forms.examples import main

class FileUploadFormPage(main.FormExamplePage):

    title = 'File Upload'
    description = 'Uploading a file'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('file', forms.File())
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print form, data
