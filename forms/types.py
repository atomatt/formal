"""
Form types.
"""

from forms import iforms, validation
from zope.interface import implements


class String(object):
    
    implements( iforms.IType )
    
    name = None
    required = False
    strip = False
    missing = None
    immutable = False
    
    def __init__(self, required=None, strip=None, missing=None, immutable=False):
        if required is not None: 
            self.required = required
        if strip is not None:
            self.strip = strip
        if missing is not None:
            self.missing = missing
        self.immutable = immutable
        
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
    
    implements( iforms.IType )
    
    name = None
    required = False
    missing = None
    immutable = False
   
    def __init__(self, required=None, missing=None, immutable=False):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        self.immutable = immutable
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Float(object):
    
    implements( iforms.IType )
    
    name = None
    required = False
    missing = None
    immutable = False
    
    def __init__(self, required=None, missing=None, immutable=False):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        self.immutable = immutable
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Boolean(object):
    
    implements( iforms.IType )
    
    name = None
    required = False
    missing = None
    immutable = False
    
    def __init__(self, required=None, missing=None, immutable=False):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        self.immutable = immutable

    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Date(object):
    
    implements( iforms.IType )
    
    name = None
    required = None
    missing = None
    immutable = False
    
    def __init__(self, required=None, missing=None, immutable=False):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        self.immutable = immutable
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Time(object):
    
    implements( iforms.IType )
    
    name = None
    required = None 
    missing = None
    immutable = False
        
    def __init__(self, required=None, missing=None, immutable=False):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        self.immutable = immutable
            
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value
        
        
class Sequence(object):
    implements( iforms.IType )
    
    name = None
    required = None 
    missing = None
    type = None
    immutable = False

    def __init__(self, type=None, required=None, missing=None, immutable=False):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        if type is not None:
            self.type = type
        self.immutable = immutable
            
    def validate(self, value):
        if self.required and not value:
            raise validation.FieldRequiredError('needs at least one item checked')
        if value is None:
            value = self.missing
        return value


class File(object):
    implements( iforms.IType )
    
    name = None
    required = False
    missing = None
    immutable = False
   
    def __init__(self, required=None, missing=None, immutable=False):
        if required is not None:
            self.required = required
        if missing is not None:
            self.missing = missing
        self.immutable = immutable
        
    def validate(self, value):
        if self.required and value is None:
            raise validation.FieldRequiredError('required field')
        if value is None:
            value = self.missing
        return value



__all__ = [
    'Boolean', 'Date', 'File', 'Float', 'Integer', 'Sequence', 'String', 'Time',
    ]
    
