"""Adapters for converting to and from a type's value according to an
IConvertible protocol.
"""

from datetime import date, time
from nevow.compy import Adapter
from forms import iforms, validation
from zope.interface import implements


class NullConverter(Adapter):
    implements( iforms.IStringConvertible )
    
    def fromType(self, value):
        if value is None:
            return None
        return value
    
    def toType(self, value):
        if value is None:
            return None
        return value


class NumberToStringConverter(Adapter):
    implements( iforms.IStringConvertible )
    cast = None
    
    def fromType(self, value):
        if value is None:
            return None
        return str(value)
    
    def toType(self, value):
        if value is not None:
            value = value.strip()
        if not value:
            return None
        try:
            value = self.cast(value)
        except ValueError:
            raise validation.FieldValidationError("Not a valid number")
        return value
        
        
class IntegerToStringConverter(NumberToStringConverter):
    cast = int


class FloatToStringConverter(NumberToStringConverter):
    cast = float


class BooleanToStringConverter(Adapter):
    implements( iforms.IStringConvertible )
    
    def fromType(self, value):
        if value is None:
            return None
        if value:
            return 'True'
        return 'False'
        
    def toType(self, value):
        if value is not None:
            value = value.strip()
        if not value:
            return None
        if value not in ('True', 'False'):
            raise validation.FieldValidationError('%r should be either True or False')
        return value == 'True'
    
    
class DateToStringConverter(Adapter):
    implements( iforms.IStringConvertible )
    
    def fromType(self, value):
        if value is None:
            return None
        return value.isoformat()
    
    def toType(self, value):
        if value is not None:
            value = value.strip()
        if not value:
            return None
        return self.parseDate(value)
        
    def parseDate(self, value):
        try:
            y, m, d = [int(p) for p in value.split('-')]
        except ValueError:
            raise validation.FieldValidationError('Invalid date')
        try:
            value = date(y, m, d)
        except ValueError, e:
            raise validation.FieldValidationError('Invalid date: '+str(e))
        return value


class TimeToStringConverter(Adapter):
    implements( iforms.IStringConvertible )
    
    def fromType(self, value):
        if value is None:
            return None
        return value.isoformat()
    
    def toType(self, value):
        if value is not None:
            value = value.strip()
        if not value:
            return None
        return self.parseTime(value)
        
    def parseTime(self, value):
        
        if '.' in value:
            value, ms = value.split('.')
        else:
            ms = 0
            
        try:
            h, m, s = value.split(':')  
            h, m, s, ms = int(h), int(m), int(s), int(ms)
        except:
            raise validation.FieldValidationError('Invalid time')
        
        try:
            value = time(h, m, s, ms)
        except ValueError, e:
            raise validation.FieldValidationError('Invalid time: '+str(e))
            
        return value
        
        
class DateToDateTupleConverter(Adapter):
    implements( iforms.IDateTupleConvertible )
    
    def fromType(self, value):
        if value is None:
            return None, None, None
        return value.year, value.month, value.day
        
    def toType(self, value):
        if value is None:
            return None
        try:
            value = date(*value)
        except (TypeError, ValueError), e:
            raise validation.FieldValidationError('Invalid date: '+str(e))
        return value
        
