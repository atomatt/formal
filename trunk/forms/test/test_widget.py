from twisted.trial import unittest
from nevow import context, flat, inevow
import forms
from forms import iforms
from zope.interface import implements


skip = "All the widget tests need rewriting :-/"


class FakeRequest(object):
    implements( inevow.IRequest )
    
    uri = '/'
    received_headers = {}
    
    def __init__(self, **k):
        super(FakeRequest, self).__init__()
        self.args = k
        
    def prePathURL(self):
        return '/'
        
        
class FakeForm(object):
    implements( iforms.IForm )
    
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data


class FormFactory(object):
    implements( iforms.IFormFactory )
    
    def __init__(self, form, *a, **k):
        super(FormFactory,self).__init__(*a, **k)
        self.form = form
    
    def formFactory(self, ctx, name):
        return self.form
        
        
def renderWidget(widget, name, data=None):
    ctx = context.RequestContext(tag=FakeRequest())
    ctx.remember(None, inevow.IData)
    return flat.flatten(iforms.IWidget(widget).render(ctx, name, {name:'bar'}, None), ctx)    
        

def processInput(widget, name, data=None):
    ctx = context.RequestContext(tag=FakeRequest())
    return widget.processInput(ctx, name, {name: data})    
        

class TestTextInput(unittest.TestCase):
    
    def test_render(self):
        r = renderWidget(forms.TextInput(forms.String()), 'foo', 'bar')
        self.assert_('<input' in r)
        self.assert_('type="text"' in r)
        self.assert_('name="foo"' in r)
        self.assert_('value="bar"' in r)
        
        
class TestUnicode(unittest.TestCase):
    
    def simpleTextWidgetTest(type):
        def test(self):
            r = processInput(type(forms.String()), 'foo', ['bar'])
            self.assert_(r == u'bar')
            r = processInput(type(forms.String()), 'foo', ['\xc2\xa3'])
            self.assert_(r == u'\xa3')
        test.func_name = 'test_%s'%type.__name__
        return test

    test_TextInput = simpleTextWidgetTest(forms.TextInput)
    test_Password = simpleTextWidgetTest(forms.Password)
    test_TextArea = simpleTextWidgetTest(forms.TextArea)
    
