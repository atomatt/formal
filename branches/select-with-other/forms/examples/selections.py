from twisted.internet import defer
from datetime import date
import forms
from forms.examples import main

# A boring list of (value, label) pairs.
strings = [
    ('foo', 'Foo'),
    ('bar', 'Bar'),
    ]

# A list of dates with meaningful names.
dates = [
    (date(2005, 01, 01), 'New Year Day'),
    (date(2005, 11, 06), 'My Birthday'),
    (date(2005, 12, 25), 'Christmas Day'),
    ]

def data_strings(ctx, data):
    # Let's defer it, just for fun.
    return defer.succeed(strings)
    
# A different "none" option tuple
differentNone = ('none value', '- select -')
    
class SelectionFormPage(main.FormExamplePage):

    title = 'Selection widgets'
    description = 'Example of the various selection widgets'
    
    def form_example(self, ctx):
        form = forms.Form()
        form.addField('required', forms.String(required=True))
        """
        form.addField('oneString', forms.String(), forms.widgetFactory(forms.SelectChoice, options=strings))
        form.addField('anotherString', forms.String(), forms.widgetFactory(forms.SelectChoice, options=data_strings))
        form.addField('oneMoreString', forms.String(required=True), forms.widgetFactory(forms.RadioChoice, options=data_strings))
        form.addField('oneDate', forms.Date(), forms.widgetFactory(forms.SelectChoice, options=dates))
        form.addField('multipleStrings', forms.Sequence(forms.String()), forms.widgetFactory(forms.CheckboxMultiChoice, options=strings))
        form.addField('multipleDates', forms.Sequence(forms.Date()), forms.widgetFactory(forms.CheckboxMultiChoice, options=dates))
        form.addField('differentNoneSelect', forms.String(), forms.widgetFactory(forms.SelectChoice, options=strings, noneOption=differentNone))
        form.addField('differentNoneRadios', forms.String(), forms.widgetFactory(forms.RadioChoice, options=data_strings, noneOption=differentNone))
        """
        form.addField('selectOther', forms.String(), forms.widgetFactory(forms.SelectOtherChoice, options=['Mr', 'Mrs']))
        form.addField('selectOtherRequired', forms.String(required=True), forms.widgetFactory(forms.SelectOtherChoice, options=['Mr', 'Mrs']))
        form.addAction(self.submitted)
        return form
    
    def submitted(self, ctx, form, data):
        print form, data
