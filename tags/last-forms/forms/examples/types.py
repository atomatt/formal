try:
    import decimal
    haveDecimal = True
except ImportError:
    haveDecimal = False
import forms
from forms.examples import main

class TypesFormPage(main.FormExamplePage):

    title = 'Form Types'
    description = 'Example of using different typed fields.'

    def form_example(self, ctx):
        form = forms.Form()
        form.addField('aString', forms.String())
        form.addField('aInteger', forms.Integer())
        form.addField('aFloat', forms.Float())
        if haveDecimal:
            form.addField('aDecimal', forms.Decimal())
        form.addField('aBoolean', forms.Boolean())
        form.addField('aDate', forms.Date())
        form.addField('aTime', forms.Time())
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print data

