from datetime import date, time
from twisted.trial import unittest
from forms import converters, validation


class TestConverters(unittest.TestCase):
    
    def test_null(self):
        c = converters.NullConverter(None)
        self.assertEquals(c.fromType('foo'), 'foo')
        self.assertEquals(c.toType('foo'), 'foo')
        
    def test_integerToString(self):
        c = converters.IntegerToStringConverter(None)
        self.assertEquals(c.fromType(None), None)
        self.assertEquals(c.fromType(1), '1')
        self.assertEquals(c.fromType(0), '0')
        self.assertEquals(c.fromType(-1), '-1')
        self.assertEquals(c.toType(''), None)
        self.assertEquals(c.toType(' '), None)
        self.assertEquals(c.toType('1'), 1)
        self.assertEquals(c.toType('0'), 0)
        self.assertEquals(c.toType('-1'), -1)
        self.assertRaises(validation.FieldValidationError, c.toType, '1.1')
        self.assertRaises(validation.FieldValidationError, c.toType, 'foo')

    def test_floatToString(self):
        c = converters.FloatToStringConverter(None)
        self.assertEquals(c.fromType(None), None)
        self.assertEquals(c.fromType(1), '1')
        self.assertEquals(c.fromType(0), '0')
        self.assertEquals(c.fromType(-1), '-1')
        self.assertEquals(c.fromType(1.5), '1.5')
        self.assertEquals(c.toType(''), None)
        self.assertEquals(c.toType(' '), None)
        self.assertEquals(c.toType('1'), 1)
        self.assertEquals(c.toType('0'), 0)
        self.assertEquals(c.toType('-1'), -1)
        self.assertEquals(c.toType('-1.5'), -1.5)
        self.assertRaises(validation.FieldValidationError, c.toType, 'foo')
        
    def test_booleanToString(self):
        c = converters.BooleanToStringConverter(None)
        self.assertEquals(c.fromType(False), 'False')
        self.assertEquals(c.fromType(True), 'True')
        self.assertEquals(c.fromType(None), None)
        self.assertEquals(c.toType('False'), False)
        self.assertEquals(c.toType('True'), True)
        self.assertEquals(c.toType(''), None)
        self.assertEquals(c.toType('  '), None)
        self.assertRaises(validation.FieldValidationError, c.toType, 'foo')
        
    def test_dateToString(self):
        c = converters.DateToStringConverter(None)
        self.assertEquals(c.fromType(date(2005, 5, 6)), '2005-05-06')
        self.assertEquals(c.fromType(date(2005, 1, 1)), '2005-01-01')
        self.assertEquals(c.toType(''), None)
        self.assertEquals(c.toType(' '), None)
        self.assertEquals(c.toType('2005-05-06'), date(2005, 5, 6))
        self.assertEquals(c.toType('2005-01-01'), date(2005, 1, 1))
        self.assertRaises(validation.FieldValidationError, c.toType, 'foo')
        self.assertRaises(validation.FieldValidationError, c.toType, '2005')
        self.assertRaises(validation.FieldValidationError, c.toType, '01/01/2005')
        self.assertRaises(validation.FieldValidationError, c.toType, '01-01-2005')
        
    def test_timeToString(self):
        c = converters.TimeToStringConverter(None)
        self.assertEquals(c.fromType(time(12, 56)), '12:56:00')
        self.assertEquals(c.fromType(time(10, 12, 24)), '10:12:24')
        self.assertEquals(c.toType(''), None)
        self.assertEquals(c.toType(' '), None)
        self.assertEquals(c.toType('12:56:00'), time(12, 56))
        self.assertEquals(c.toType('10:12:24'), time(10, 12, 24))
        self.assertRaises(validation.FieldValidationError, c.toType, 'foo')
        self.assertRaises(validation.FieldValidationError, c.toType, '10')
        self.assertRaises(validation.FieldValidationError, c.toType, '10-12')
        
    def test_dateToTuple(self):
        c = converters.DateToDateTupleConverter(None)
        self.assertEquals(c.fromType(date(2005, 5, 6)), (2005, 5, 6))
        self.assertEquals(c.fromType(date(2005, 1, 1)), (2005, 1, 1))
        self.assertEquals(c.toType((2005, 5, 6)), date(2005, 5, 6))
        self.assertEquals(c.toType((2005, 1, 1)), date(2005, 1, 1))
        self.assertRaises(validation.FieldValidationError, c.toType, ('foo'))
        self.assertRaises(validation.FieldValidationError, c.toType, (2005,))
        self.assertRaises(validation.FieldValidationError, c.toType, (2005,10))
        self.assertRaises(validation.FieldValidationError, c.toType, (1, 1, 2005))
        
