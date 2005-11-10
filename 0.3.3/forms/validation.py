import re
from zope.interface import implements
from forms import iforms


class FormError(Exception):
    pass
    
    
class FieldError(Exception):
    def __init__(self, message, fieldName=None):
        Exception.__init__(self, message)
        self.message = message
        self.fieldName = fieldName
    
    
class FieldValidationError(FieldError):
    pass
    
    
class FieldRequiredError(FieldValidationError):
    pass
    
    
class RequiredValidator(object):
    implements(iforms.IValidator)
    
    def validate(self, field, value):
        if value is None:
            raise FieldRequiredError, 'Required'

    
class LengthValidator(object):
    """Validate the length of the value is within a given range. 
    """
    implements(iforms.IValidator)
    
    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max
        assert self.min is not None or self.max is not None
        
    def validationErrorMessage(self, field):
        if self.min is not None and self.max is None:
            return 'Must be longer than %r characters'%(self.min,)
        if self.min is None and self.max is not None:
            return 'Must be shorter than %r characters'%(self.max,)
        return 'Must be between %r and %r characters'%(self.min, self.max)
    
    def validate(self, field, value):
        if value is None:
            return
        length = len(value)
        if self.min is not None and length < self.min:
            raise FieldValidationError, self.validationErrorMessage(field)
        if self.max is not None and length > self.max:
            raise FieldValidationError, self.validationErrorMessage(field)
            
            
class RangeValidator(object):
    """Validate the size of the value is within is given range.
    """
    implements(iforms.IValidator)
    
    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max
        assert self.min is not None or self.max is not None
        
    def validationErrorMessage(self, field):
        if self.min is not None and self.max is None:
            return 'Must be greater than %r'%(self.min,)
        if self.min is None and self.max is not None:
            return 'Must be less than %r'%(self.max,)
        return 'Must be between %r and %r'%(self.min, self.max)
    
    def validate(self, field, value):
        if value is None:
            return
        if self.min is not None and value < self.min:
            raise FieldValidationError, self.validationErrorMessage(field)
        if self.max is not None and value > self.max:
            raise FieldValidationError, self.validationErrorMessage(field)

            
class PatternValidator(object):
    """Validate the value is a certain pattern.
    
    The required pattern is defined as a regular expression. The regex will be
    compiled automatically if necessary.
    """
    implements(iforms.IValidator)
    
    def __init__(self, regex):
        self.regex = regex
        
    def validate(self, field, value):
        if value is None:
            return
        # If it doesn't look like a regex object then compile it now
        if not hasattr(self.regex, 'match'):
            self.regex = re.compile(self.regex)
        if self.regex.match(value) is None:
            raise FieldValidationError, 'Invalid format'
            
    
__all__ = [
    'FormError', 'FieldError', 'FieldValidationError', 'FieldRequiredError',
    'RequiredValidator', 'LengthValidator', 'RangeValidator', 'PatternValidator',
    ]

