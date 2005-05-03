"""
Form types.
"""

from forms import iforms, validation

"""
  - DateTime
  - Structure
  - Mapping
"""


class String(object):
    
    __implements__ = iforms.IType,
    
    name = None
    required = False
    strip = False
    missing = None
    
    def __init__(self, required=None, strip=None, missing=None):
        if required is not None: 
            self.required = required
        if strip is not None:
            self.strip = strip
        if missing is not None:
            self.missing = missing
        
    def validate(self, value):
        if value is not None and self.strip:
            value = value.strip()
        if not value:
            value = None
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Integer(object):
    
    __implements__ = iforms.IType,
    
    name = None
    required = False
    missing = None
   
    def __init__(self, required=None, missing=None):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Float(object):
    
    __implements__ = iforms.IType,
    
    name = None
    required = False
    missing = None
    
    def __init__(self, required=None, missing=None):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Boolean(object):
    
    __implements__ = iforms.IType,
    
    name = None
    required = False
    missing = None
    
    def __init__(self, required=None, missing=None):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing

    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Date(object):
    
    __implements__ = iforms.IType,
    
    name = None
    required = None
    missing = None
    
    def __init__(self, required=None, missing=None):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Time(object):
    
    __implements__ = iforms.IType,
    
    name = None
    required = None 
    missing = None
        
    def __init__(self, required=None, missing=None):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
            
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Sequence(object):
    __implements__ = iforms.IType,
    
    name = None
    required = None 
    missing = None
    type = None

    def __init__(self, type=None, required=None, missing=None):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        if type is not None:
            self.type = type
            
    def validate(self, value):
        if self.required and not value:
            raise validation.FieldRequiredError('needs at least one item checked')
        if value is None:
            value = self.missing
        return value


class File(object):
    __implements__ = iforms.IType,
    
    name = None
    required = False
    missing = None
   
    def __init__(self, required=None, missing=None):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value


__all__ = [
    'Boolean', 'Date', 'File', 'Float', 'Integer', 'Sequence', 'String', 'Time',
    ]
    
