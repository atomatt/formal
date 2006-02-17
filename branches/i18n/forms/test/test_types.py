from datetime import date, time
from twisted.trial import unittest
import forms
from forms import validation


class TestValidators(unittest.TestCase):

    def testHasValidator(self):
        t = forms.String(validators=[validation.LengthValidator(max=10)])
        self.assertEquals(t.hasValidator(validation.LengthValidator), True)

    def testRequired(self):
        t = forms.String(required=True)
        self.assertEquals(t.hasValidator(validation.RequiredValidator), True)
        self.assertEquals(t.required, True)


class TestCreation(unittest.TestCase):

    def test_immutablility(self):
        self.assertEquals(forms.String().immutable, False)
        self.assertEquals(forms.String(immutable=False).immutable, False)
        self.assertEquals(forms.String(immutable=True).immutable, True)

    def test_immutablilityOverride(self):
        class String(forms.String):
            immutable = True
        self.assertEquals(String().immutable, True)
        self.assertEquals(String(immutable=False).immutable, False)
        self.assertEquals(String(immutable=True).immutable, True)


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
        self.assertRaises(forms.FieldValidationError, forms.String(required=True).validate, '')
        self.assertRaises(forms.FieldValidationError, forms.String(required=True).validate, None)

    def testInteger(self):
        self.assertEquals(forms.Integer().validate(None), None)
        self.assertEquals(forms.Integer().validate(0), 0)
        self.assertEquals(forms.Integer().validate(1), 1)
        self.assertEquals(forms.Integer().validate(-1), -1)
        self.assertEquals(forms.Integer(missing=1).validate(None), 1)
        self.assertEquals(forms.Integer(missing=1).validate(2), 2)
        self.assertRaises(forms.FieldValidationError, forms.Integer(required=True).validate, None)

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
        self.assertRaises(forms.FieldValidationError, forms.Float(required=True).validate, None)

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
        self.assertRaises(forms.FieldValidationError, forms.Date(required=True).validate, None)

    def testTime(self):
        self.assertEquals(forms.Time().validate(None), None)
        self.assertEquals(forms.Time().validate(time(12,30,30)), time(12,30,30))
        self.assertEquals(forms.Time(missing=time(12,30,30)).validate(None), time(12,30,30))
        self.assertEquals(forms.Time(missing=time(12,30,30)).validate(time(12,30,31)), time(12,30,31))
        self.assertRaises(forms.FieldValidationError, forms.Time(required=True).validate, None)

    def test_sequence(self):
        self.assertEquals(forms.Sequence(forms.String()).validate(None), None)
        self.assertEquals(forms.Sequence(forms.String()).validate(['foo']), ['foo'])
        self.assertEquals(forms.Sequence(forms.String(), missing=['foo']).validate(None), ['foo'])
        self.assertEquals(forms.Sequence(forms.String(), missing=['foo']).validate(['bar']), ['bar'])
        self.assertRaises(forms.FieldValidationError, forms.Sequence(forms.String(), required=True).validate, None)
        self.assertRaises(forms.FieldValidationError, forms.Sequence(forms.String(), required=True).validate, [])

    def test_file(self):
        pass
    test_file.skip = "write tests"

