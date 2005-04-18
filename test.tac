from datetime import date, time
from twisted.application import internet, service
from nevow import appserver, compy, loaders, rend, static, tags as T
import forms
from forms import iforms, htmleditor


dates = [
    (date(2005,1,1), 'New year\'s day'),
    (date(2005,11,6), 'My birthday'),
    (date(2005,12,25), 'Christmas day'),
    ]
    
times = [
    (time(5,0), 'Really early'),
    (time(7,0), 'A bit too early'),
    (time(8,0), 'Hmm, not bad'),
    (time(10,0), 'Nice :)'),
    ]
    
    
class Person(object):
    
    def __init__(self, id, firstName, lastName):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        
        
class PersonKeyLabelAdapter(object):
    __implements__ = iforms.IKey, iforms.ILabel
    
    def __init__(self, original):
        self.original = original
        
    def key(self):
        return self.original.id
        
    def label(self):
        return '%s, %s' % (self.original.lastName, self.original.firstName)
        
        
compy.registerAdapter(PersonKeyLabelAdapter, Person, iforms.IKey)
compy.registerAdapter(PersonKeyLabelAdapter, Person, iforms.ILabel)
    
    
people = [
    Person(1, 'Matt', 'Goodall'),
    Person(2, 'Tim', 'Parkin'),
    ]


class Page(rend.Page, forms.ResourceMixin):
    
    addSlash = True
    docFactory = loaders.xmlfile('test.html')
        
    def __init__(self, *a, **k):
        rend.Page.__init__(self, *a, **k)
        forms.ResourceMixin.__init__(self)
        
    def child_self(self, ctx):
        return self

    def form_oneOfEach(self, ctx):
        form = forms.Form(self._submit)
        form.addField('string', forms.String(required=True))
        form.addField('password', forms.String(), forms.CheckedPassword)
        form.addField('integer', forms.Integer())
        form.addField('float', forms.Float())
        form.addField('boolean', forms.Boolean())
        form.addField('date', forms.Date(), forms.widgetFactory(forms.MMYYDatePartsInput, cutoffYear=38))
        form.addField('time', forms.Time())
        form.addAction(self._submit)
        return form

    def form_test(self, ctx):
        form = forms.Form(self._submit)
        form.addField('lastName', forms.String(required=True), label='Surname', description='This should be used to store your surname.. no really!!')
        form.addField('date', forms.Date(), forms.widgetFactory(forms.SelectChoice, dates))
        form.addField('time', forms.Time(), lambda original: forms.SelectChoice(original, times))
        form.addField('author', forms.Integer(), lambda original: forms.SelectChoice(original, people))
        form.addField('notes', forms.String(), htmleditor.TinyMCE)
        form.addField('foo', forms.Sequence(forms.Time()), forms.widgetFactory(forms.CheckboxMultiChoice, times))
        form.addField('bar', forms.Sequence(forms.String(),required=True), forms.widgetFactory(forms.CheckboxMultiChoice, zip('abc','abc')),description='store your bar here')
        form.data = {'foo': [time(10,0)]}
        form.addAction(self._submit)
        form.addAction(self._submit, 'another')
        return form
        
    def form_1(self, ctx):
        form = forms.Form(self._submit)
        form.addField('name', forms.String(required=True))
        form.addAction(self._submit)
        form.data = {
            'name': 'Me!'
            }
        return form
        
    def form_2(self, ctx):
        form = forms.Form(self._submit)
        form.addField('name', forms.String(required=True))
        form.addAction(self._submit)
        form.data = {
            'name': 'Me!'
            }
        return form
        
    def _submit(self, ctx, form, data):
        print form
        print data
        if data.get('string') == 'error':
            raise forms.FieldError('Failed the field!', 'string')
        if data.get('string') == 'formerror':
            raise forms.FormError('Failed the form!')
        
setattr(Page, 'child_nevow-forms.css', forms.defaultCSS)
setattr(Page, 'child_tiny_mce', static.File('tiny_mce'))
        
        
root = Page()
site = appserver.NevowSite(root, logPath='/dev/null')
application = service.Application('forms2-test')
internet.TCPServer(8000, site).setServiceParent(application)

