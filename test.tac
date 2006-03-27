from datetime import date, time
from twisted.application import internet, service
from nevow import appserver, compy, loaders, rend, static, tags as T
import formal
import os
from shutil import copyfileobj
import mimetypes, datetime

from formal import iformal, htmleditor, converters
from fileresource import fileResource

class KeyToFileConverter( object ):
    __implements__ = iformal.IFileConvertible,

    def fromType( self, value, context=None ):
        """
            Given a string generate a (mimetype, filelike, fileName) or None
        """
        if not value or value == '':
            return None

        mimetype = mimetypes.guess_type( value )
        filelike = open(os.path.join('images',value),'r')
        return (mimetype, filelike, value)

    def toType( self, value ):
        """
            Given a (mimetype, filelike, filename) tuple return a string
        """
        if not value:
            return None

        (mimetype, filelike,fileName) = value;
        target = file(os.path.join('images',fileName),'w')
        copyfileobj( filelike, target )
        target.close()
        filelike.close()
        return fileName


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
    __implements__ = iformal.IKey, iformal.ILabel
    
    def __init__(self, original):
        self.original = original
        
    def key(self):
        return self.original.id
        
    def label(self):
        return '%s, %s' % (self.original.lastName, self.original.firstName)
        
        
compy.registerAdapter(PersonKeyLabelAdapter, Person, iformal.IKey)
compy.registerAdapter(PersonKeyLabelAdapter, Person, iformal.ILabel)
    
    
people = [
    Person(1, 'Matt', 'Goodall'),
    Person(2, 'Tim', 'Parkin'),
    ]

class Page(rend.Page, formal.ResourceMixin):
    
    addSlash = True
    docFactory = loaders.xmlfile('test.html')
        
    def __init__(self, *a, **k):
        rend.Page.__init__(self, *a, **k)
        formal.ResourceMixin.__init__(self)
        
    def child_self(self, ctx):
        return self

    def form_oneOfEach(self, ctx):
        form = formal.Form(self._submit)
        form.addField('hidden_string', formal.Integer(), formal.Hidden)
        form.addField('string', formal.String(required=True))
        form.addField('password', formal.String(), formal.CheckedPassword)
        form.addField('integer', formal.Integer())
        form.addField('float', formal.Float())
        form.addField('boolean', formal.Boolean())
        form.addField('date', formal.Date(), formal.widgetFactory(formal.MMYYDatePartsInput, cutoffYear=38))
        form.addField('time', formal.Time())
        form.addAction(self._submit)
        form.data = {'hidden_string': 101}
        return form

    def form_readonlyOneOfEach(self, ctx):
        form = formal.Form(self._submit)
        immutable=True
        form.addField('string', formal.String(immutable=immutable), formal.TextInput)
        form.addField('textarea', formal.String(immutable=immutable), formal.TextArea)
        form.addField('password', formal.String(immutable=immutable), formal.CheckedPassword)
        form.addField('integer', formal.Integer(immutable=immutable))
        form.addField('float', formal.Float(immutable=immutable))
        form.addField('boolean', formal.Boolean(immutable=immutable), formal.Checkbox)
        form.addField('date', formal.Date(immutable=immutable), formal.widgetFactory(formal.MMYYDatePartsInput, cutoffYear=38))
        form.addField('date2', formal.Date(immutable=immutable), formal.widgetFactory(formal.DatePartsInput, dayFirst=True))
        form.addField('time', formal.Time(immutable=immutable))
        form.addField('author', formal.Integer(immutable=immutable), lambda original: formal.SelectChoice(original, people))
        form.addField('bar', formal.Sequence(formal.String(),immutable=immutable), formal.widgetFactory(formal.CheckboxMultiChoice, zip('abc','abc')),description='store your bar here')
        form.addField('file', formal.File(immutable=immutable), formal.widgetFactory(formal.FileUploadWidget, convertibleFactory=KeyToFileConverter))
        form.addAction(self._submit)
        form.data = {'string':'hello', 'textarea':'some long text', 'password': ['one','one'], 'integer':10, 'float':22.22, 'boolean':True, 'author': 2, 'file':'dm.gif', 'date': datetime.date(2005, 10, 1), 'bar': ['a'], 'time': datetime.time(12, 51, 30)}

        return form

    def form_test(self, ctx):
        form = formal.Form(self._submit)
        form.addField('lastName', formal.String(required=True), label='Surname', description='This should be used to store your surname.. no really!!')
        form.addField('date', formal.Date(), formal.widgetFactory(formal.SelectChoice, dates))
        form.addField('time', formal.Time(), lambda original: formal.SelectChoice(original, times))
        form.addField('author', formal.Integer(), lambda original: formal.SelectChoice(original, people))
        form.addField('notes', formal.String(), htmleditor.TinyMCE)
        form.addField('foo', formal.Sequence(formal.Time()), formal.widgetFactory(formal.CheckboxMultiChoice, times))
        form.addField('bar', formal.Sequence(formal.String(),required=True), formal.widgetFactory(formal.CheckboxMultiChoice, zip('abc','abc')),description='store your bar here')
        form.data = {'foo': [time(10,0)]}
        form.addAction(self._submit)
        form.addAction(self._submit, 'another')
        return form
        
    def form_1(self, ctx):
        form = formal.Form(self._submit)
        form.addField('name', formal.String(required=True))
        form.addAction(self._submit)
        form.data = {
            'name': 'Me!'
            }
        return form
        
    def form_2(self, ctx):
        form = formal.Form(self._submit)
        form.addField('name', formal.String(required=True))
        form.addAction(self._submit)
        form.data = {
            'name': 'Me!'
            }
        return form
        
    def form_3(self, ctx):
        ''' This test needs an 'assets' folder to store files in. The widget is passed a fileResource which 
            is used to get a preview url and to save the upload results. commit/rollback type hooks will need
            to be added to forms to allow 'clean' operation. -- tp
        '''
        form = formal.Form(self._submit)
        form.addField('name', formal.String(required=True))
        form.addField('file', formal.String(required=True), formal.widgetFactory(formal.FileUpload,fileResource(),preview='image'))
        form.addAction(self._submit)
        #form.data = {
        #    'file': 'product.jpg'
        #    }
        return form        

    def form_4(self, ctx):
        form = formal.Form(self._submit)
        form.addField('name', formal.String(required=True))
        form.addField('file', formal.File(required=True), formal.widgetFactory(formal.FileUploadWidget, convertibleFactory=KeyToFileConverter))
        form.addAction(self._submit)
#        form.data = {
#            'file': 'dm.gif'
#            }
        return form        
    
    def _submit(self, ctx, form, data):
        print form
        print data
        if data.get('string') == 'error':
            raise formal.FieldError('Failed the field!', 'string')
        if data.get('string') == 'formerror':
            raise formal.FormError('Failed the form!')

setattr(Page, 'child_nevow-forms.css', formal.defaultCSS)
setattr(Page, 'child_tiny_mce', static.File('tiny_mce'))
setattr(Page, 'child_webassets', static.File('assets'))
setattr(Page, 'child_images', static.File('images'))
setattr(Page, 'child_uploads', static.File('uploads'))

root = Page()
site = appserver.NevowSite(root, logPath='/dev/null')
application = service.Application('forms2-test')
internet.TCPServer(8000, site).setServiceParent(application)

