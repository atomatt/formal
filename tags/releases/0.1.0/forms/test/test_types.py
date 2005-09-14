from datetime import date, time
from twisted.trial import unittest
import forms


class TestValidate(unittest.TestCase):
    
    def testString(self):
        self.assertEquals(forms.String().validate(None), None)
        self.assertEquals(forms.String().validate(''), None)
        self.assertEquals(forms.String().validate(' '), ' ')
        self.assertEquals(forms.String().validate('foo'), 'foo')
        self.assertEquals(forms.String().validate(u'foo'), u'foo')
        self.assertEquals(forms.String(strip=True).validate(' '), None)
        self.assertEquals(forms.String(strip=True).validate(' foo '), 'foo')
        self.assertEquals(forms.String(missing='bar').validate('foo'), 'foo')
        self.assertEquals(forms.String(missing='bar').validate(''), 'bar')
        self.assertEquals(forms.String(strip=True, missing='').validate(' '), '')
        self.assertEquals(forms.String(missing='foo').validate('bar'), 'bar')

    def testInteger(self):
        self.assertEquals(forms.Integer().validate(None), None)
        self.assertEquals(forms.Integer().validate(0), 0)
        self.assertEquals(forms.Integer().validate(1), 1)
        self.assertEquals(forms.Integer().validate(-1), -1)
        self.assertEquals(forms.Integer(missing=1).validate(None), 1)
        self.assertEquals(forms.Integer(missing=1).validate(2), 2)
        
    def testFloat(self):
        self.assertEquals(forms.Float().validate(None), None)
        self.assertEquals(forms.Float().validate(0), 0.0)
        self.assertEquals(forms.Float().validate(0.0), 0.0)
        self.assertEquals(forms.Float().validate(.1), 0.1)
        self.assertEquals(forms.Float().validate(1), 1.0)
        self.assertEquals(forms.Float().validate(-1), -1.0)
        self.assertEquals(forms.Float().validate(-1.86), -1.86)
        self.assertEquals(forms.Float(missing=1.0).validate(None), 1.0)
        self.assertEquals(forms.Float(missing=1.0).validate(2.0), 2.0)
                
    def testBoolean(self):
        self.assertEquals(forms.Boolean().validate(None), None)
        self.assertEquals(forms.Boolean().validate(True), True)
        self.assertEquals(forms.Boolean().validate(False), False)
        self.assertEquals(forms.Boolean(missing=True).validate(None), True)
        self.assertEquals(forms.Boolean(missing=True).validate(False), False)
        
    def testDate(self):
        self.assertEquals(forms.Date().validate(None), None)
        self.assertEquals(forms.Date().validate(date(2005,1,1)), date(2005,1,1))
        self.assertEquals(forms.Date(missing=date(2005,1,2)).validate(None), date(2005,1,2))
        self.assertEquals(forms.Date(missing=date(2005,1,2)).validate(date(2005,1,1)), date(2005,1,1))
        
    def testTime(self):
        self.assertEquals(forms.Time().validate(None), None)
        self.assertEquals(forms.Time().validate(time(12,30,30)), time(12,30,30))
        self.assertEquals(forms.Time(missing=time(12,30,30)).validate(None), time(12,30,30))
        self.assertEquals(forms.Time(missing=time(12,30,30)).validate(time(12,30,31)), time(12,30,31))
        
    def test_sequence(self):
        self.assertEquals(forms.Sequence(forms.String()).validate(None), None)
        self.assertEquals(forms.Sequence(forms.String()).validate(['foo']), ['foo'])
        self.assertEquals(forms.Sequence(forms.String(), missing=['foo']).validate(None), ['foo'])
        self.assertEquals(forms.Sequence(forms.String(), missing=['foo']).validate(['bar']), ['bar'])
    
    def test_file(self):
        pass
    test_file.skip = "write tests"
    
