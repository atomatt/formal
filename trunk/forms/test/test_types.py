from datetime import date, time, datetime
from twisted.trial import unittest
import forms


class FakeContext(object):
    pass


class TestToPython(unittest.TestCase):
    
    def testString(self):
        ctx = FakeContext()
        self.assertEquals(forms.String().toPython(None), None)
        self.assertEquals(forms.String().toPython(''), None)
        self.assertEquals(forms.String().toPython(' '), ' ')
        self.assertEquals(forms.String().toPython('foo'), 'foo')
        self.assertEquals(forms.String().toPython(u'foo'), u'foo')
        self.assertEquals(forms.String(strip=True).toPython(' '), None)
        self.assertEquals(forms.String(strip=True).toPython(' foo '), 'foo')
        self.assertEquals(forms.String(missing='bar').toPython('foo'), 'foo')
        self.assertEquals(forms.String(missing='bar').toPython(''), 'bar')

    def testInteger(self):
        ctx = FakeContext()
        self.assertEquals(forms.Integer().toPython(None), None)
        self.assertEquals(forms.Integer().toPython(''), None)
        self.assertEquals(forms.Integer().toPython(' '), None)
        self.assertEquals(forms.Integer().toPython('0'), 0)
        self.assertEquals(forms.Integer().toPython('1'), 1)
        self.assertEquals(forms.Integer().toPython(u'1'), 1)
        self.assertEquals(forms.Integer().toPython('-1'), -1)
        self.assertEquals(forms.Integer(missing=1).toPython(''), 1)
        self.assertRaises(forms.FieldValidationError, forms.Integer().toPython, '1.0')
        self.assertRaises(forms.FieldValidationError, forms.Integer().toPython, 'abc')
        
    def testFloat(self):
        ctx = FakeContext()
        self.assertEquals(forms.Float().toPython(None), None)
        self.assertEquals(forms.Float().toPython(''), None)
        self.assertEquals(forms.Float().toPython(' '), None)
        self.assertEquals(forms.Float().toPython('0'), 0.0)
        self.assertEquals(forms.Float().toPython('0.0'), 0.0)
        self.assertEquals(forms.Float().toPython('.1'), 0.1)
        self.assertEquals(forms.Float().toPython('0.1'), 0.1)
        self.assertEquals(forms.Float().toPython('1'), 1.0)
        self.assertEquals(forms.Float().toPython(' 1 '), 1.0)
        self.assertEquals(forms.Float().toPython(u'1'), 1.0)
        self.assertEquals(forms.Float().toPython('-1'), -1.0)
        self.assertEquals(forms.Float().toPython('-1.86'), -1.86)
        self.assertEquals(forms.Float(missing=1.0).toPython(''), 1.0)
        self.assertRaises(forms.FieldValidationError, forms.Float().toPython ,'abc')
        self.assertRaises(forms.FieldValidationError, forms.Float().toPython ,'.')
        self.assertRaises(forms.FieldValidationError, forms.Float().toPython ,'1.1.1')
                
    def testBoolean(self):
        ctx = FakeContext()
        self.assertEquals(forms.Boolean().toPython(None), None)
        self.assertEquals(forms.Boolean().toPython(''), None)
        self.assertEquals(forms.Boolean().toPython(' '), None)
        self.assertEquals(forms.Boolean().toPython('True'), True)
        self.assertEquals(forms.Boolean().toPython('False'), False)
        self.assertEquals(forms.Boolean(missing=True).toPython(''), True)
        self.assertRaises(forms.FieldValidationError, forms.Boolean().toPython ,'1')
        self.assertRaises(forms.FieldValidationError, forms.Boolean().toPython ,'abc')
        
    def testDate(self):
        ctx = FakeContext()
        self.assertEquals(forms.Date().toPython(None), None)
        self.assertEquals(forms.Date().toPython(''), None)
        self.assertEquals(forms.Date().toPython('2005-01-01'), date(2005,1,1))
        self.assertEquals(forms.Date(missing=date(2005,1,2)).toPython(''), date(2005,1,2))
        self.assertEquals(forms.Date(missing=date(2005,1,2)).toPython('2005-01-01'), date(2005,1,1))
        self.assertRaises(forms.FieldValidationError, forms.Date().toPython ,'1')
        self.assertRaises(forms.FieldValidationError, forms.Date().toPython ,'abc')
        self.assertRaises(forms.FieldValidationError, forms.Date().toPython ,'2005-13-01')
        
    def testTime(self):
        ctx = FakeContext()
        self.assertEquals(forms.Time().toPython(None), None)
        self.assertEquals(forms.Time().toPython(''), None)
        self.assertEquals(forms.Time().toPython('12:30:00'), time(12,30))
        self.assertEquals(forms.Time(missing=time(12,30,30)).toPython(''), time(12,30,30))
        self.assertEquals(forms.Time(missing=time(12,30,30)).toPython('12:30:31'), time(12,30,31))
        self.assertRaises(forms.FieldValidationError, forms.Time().toPython ,'1')
        self.assertRaises(forms.FieldValidationError, forms.Time().toPython ,'abc')
        self.assertRaises(forms.FieldValidationError, forms.Time().toPython ,'35:24:98')
        
