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

    
__all__ = [
    'FormError', 'FieldError', 'FieldValidationError', 'FieldRequiredError',
    ]

