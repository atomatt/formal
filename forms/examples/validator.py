from zope.interface import implements
import forms
from forms import iforms
from forms.examples import main

# A not-too-good regex for matching an IP address.
IP_ADDRESS_PATTERN = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

class ValidatorFormPage(main.FormExamplePage):
    
    title = 'Custom form validation'
    description = 'Example of installing additional validators and writing a new one'
    
    def form_example(self, ctx):
        form = forms.Form()
        # This actually installs a RequiredValidator for you.
        form.addField('required', forms.String(required=True))
        # Exactly the same as above, only with a "manually" installed validator.
        form.addField('required2', forms.String(validators=[forms.RequiredValidator()]))
        # Check for a minimum length, if anything entered.
        form.addField('atLeastFiveChars', forms.String(validators=[forms.LengthValidator(min=5)]))
        # Check for a minimum length, if anything entered.
        form.addField('ipAddress', forms.String(strip=True, validators=[forms.PatternValidator(regex=IP_ADDRESS_PATTERN)]))
        # Check for the word 'silly'
        form.addField('silly', forms.String(validators=[SillyValidator()]))
        # Check age is between 18 and 30
        form.addField('ohToBeYoungAgain', forms.Integer(validators=[forms.RangeValidator(min=18, max=30)]))
        form.addAction(self.submitted)
        return form

    def submitted(self, ctx, form, data):
        print form, data
        
class SillyValidator(object):
    """
    A pointless example that checks a specific word, 'silly', is entered.
    """
    implements(iforms.IValidator)
    
    word = 'silly'
    
    def validate(self, field, value):
        if value is None:
            return
        if value.lower() != self.word.lower():
            raise forms.FieldValidationError('You must enter %r'%self.word)
