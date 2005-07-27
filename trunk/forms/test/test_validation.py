import re
from twisted.trial import unittest
from forms import types, validation


class TestRequired(unittest.TestCase):
    
    def test_required(self):
        v = validation.RequiredValidator()
        v.validate(types.String('foo'), 'bar')
        self.assertRaises(validation.FieldRequiredError, v.validate, types.String('foo'), None)
        
        
class TestRange(unittest.TestCase):
    
    def test_range(self):
        self.assertRaises(AssertionError, validation.RangeValidator)
        v = validation.RangeValidator(min=5, max=10)
        v.validate(types.Integer('foo'), None)
        v.validate(types.Integer('foo'), 5)
        v.validate(types.Integer('foo'), 7.5)
        v.validate(types.Integer('foo'), 10)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 0)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 4)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), -5)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 11)
        
    def test_rangeMin(self):
        v = validation.RangeValidator(min=5)
        v.validate(types.Integer('foo'), None)
        v.validate(types.Integer('foo'), 5)
        v.validate(types.Integer('foo'), 10)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 0)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 4)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), -5)
        
    def test_rangeMax(self):
        v = validation.RangeValidator(max=5)
        v.validate(types.Integer('foo'), None)
        v.validate(types.Integer('foo'), -5)
        v.validate(types.Integer('foo'), 0)
        v.validate(types.Integer('foo'), 5)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 6)
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 10)
        
        
class TestLength(unittest.TestCase):
    
    def test_length(self):
        self.assertRaises(AssertionError, validation.LengthValidator)
        v = validation.LengthValidator(min=5, max=10)
        v.validate(types.String('foo'), None)
        v.validate(types.String('foo'), '12345')
        v.validate(types.String('foo'), '1234567')
        v.validate(types.String('foo'), '1234567890')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '1234')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '12345678901')
        
    def test_lengthMin(self):
        v = validation.LengthValidator(min=5)
        v.validate(types.String('foo'), None)
        v.validate(types.String('foo'), '12345')
        v.validate(types.String('foo'), '1234567890')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '1234')
        
    def test_lengthMax(self):
        v = validation.LengthValidator(max=5)
        v.validate(types.String('foo'), None)
        v.validate(types.String('foo'), '1')
        v.validate(types.String('foo'), '12345')
        v.validate(types.String('foo'), '123')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '123456')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '1234567890')
        
        
class TestPattern(unittest.TestCase):
    
    def test_pattern(self):
        v = validation.PatternValidator('^[0-9]{3,5}$')
        v.validate(types.String('foo'), None)
        v.validate(types.String('foo'), '123')
        v.validate(types.String('foo'), '12345')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), ' 123')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '1')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 'foo')
        
    def test_regex(self):
        v = validation.PatternValidator(re.compile('^[0-9]{3,5}$'))
        v.validate(types.String('foo'), None)
        v.validate(types.String('foo'), '123')
        v.validate(types.String('foo'), '12345')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), ' 123')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), '1')
        self.assertRaises(validation.FieldValidationError, v.validate, types.String('foo'), 'foo')
        
