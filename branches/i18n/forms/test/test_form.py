from twisted.trial import unittest
import forms


class TestForm(unittest.TestCase):

    def test_fieldName(self):
        form = forms.Form()
        form.addField('foo', forms.String())
        self.assertRaises(ValueError, form.addField, 'spaceAtTheEnd ', forms.String())
        self.assertRaises(ValueError, form.addField, 'got a space in it', forms.String())
