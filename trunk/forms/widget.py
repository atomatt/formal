"""
Widgets are small components that render form fields for inputing data in a
certain format.
"""

from nevow import inevow, tags as T, util, url, static
from forms import iforms, validation
from forms.util import keytocssid
from forms.form import formWidgetResource
from zope.interface import implements
from twisted.internet import defer

# Marker object for args that are not supplied
_UNSET = object()
        
        
class TextInput(object):
    implements( iforms.IWidget )
    
    inputType = 'text'
    showValueOnFailure = True
    
    def __init__(self, original):
        self.original = original
    
    def render(self, ctx, key, args, errors):
        if errors:
            value = args.get(key, [''])[0]
        else:
            value = iforms.IStringConvertible(self.original).fromType(args.get(key))
        if not self.showValueOnFailure:
            value = None
        return T.input(type=self.inputType, name=key, id=keytocssid(ctx.key), value=value)
        
    def processInput(self, ctx, key, args):
        value = args.get(key, [''])[0].decode(util.getPOSTCharset(ctx))
        value = iforms.IStringConvertible(self.original).toType(value)
        return self.original.validate(value)
        
        
class Checkbox(object):
    implements( iforms.IWidget )
        
    def __init__(self, original):
        self.original = original
    
    def render(self, ctx, key, args, errors):
        if errors:
            value = args.get(key, [''])[0]
        else:
            value = iforms.IBooleanConvertible(self.original).fromType(args.get(key))
        tag = T.input(type='checkbox', name=key, id=keytocssid(ctx.key), value='True')
        if value == 'True':
            tag(checked='checked')
        return tag
        
    def processInput(self, ctx, key, args):
        value = args.get(key, [None])[0]
        if not value:
            value = 'False'
        value = iforms.IBooleanConvertible(self.original).toType(value)
        return self.original.validate(value)

        
class Password(TextInput):
    inputType = 'password'
    showValueOnFailure = False
    
    
class TextArea(object):
    implements( iforms.IWidget )
    
    def __init__(self, original):
        self.original = original
        
    def render(self, ctx, key, args, errors):
        if errors:
            value = args.get(key, [''])[0]
        else:
            value = iforms.IStringConvertible(self.original).fromType(args.get(key))
        return T.textarea(name=key, id=keytocssid(ctx.key))[value or '']
        
    def processInput(self, ctx, key, args):
        value = args.get(key, [''])[0].decode(util.getPOSTCharset(ctx))
        value = iforms.IStringConvertible(self.original).fromType(value)
        return self.original.validate(value)
        
        
class CheckedPassword(object):
    implements( iforms.IWidget )
    
    def __init__(self, original):
        self.original = original
    
    def render(self, ctx, key, args, errors):
        if errors and not errors.getFieldError(key):
            values = args.get(key)
        else:
            values = ('', '')
        return [
            T.input(type='password', name=key, id=keytocssid(ctx.key), value=values[0]),
            T.br,
            T.label(for_='%s__confirm'%keytocssid(ctx.key))[' Confirm '],
            T.input(type='password', name=key, id='%s__confirm'%keytocssid(ctx.key), value=values[1]),
            ]
        
    def processInput(self, ctx, key, args):
        pwds = [pwd for pwd in args.get(key, [])]
        if len(pwds) == 0:
            pwd = ''
        elif len(pwds) == 1:
            raise validation.FieldValidationError('Please enter the password twice for confirmation.')
        else:
            if pwds[0] != pwds[1]:
                raise validation.FieldValidationError('Passwords do not match.')
        return self.original.validate(pwds[0])
        
        
class SelectChoice(object):
    implements( iforms.IWidget )
    
    options = None
    noneOption = ('', '')
    
    def __init__(self, original, options=None, noneOption=_UNSET):
        self.original = original
        if options is not None:
            self.options = options
        if noneOption is not _UNSET:
            self.noneOption = noneOption
    
    def render(self, ctx, key, args, errors):
        
        converter = iforms.IStringConvertible(self.original)
        
        if errors:
            value = args.get(key, [''])[0]
        else:
            value = converter.fromType(args.get(key))
            
        def renderOptions(ctx, data):
            if self.noneOption is not None:
                yield T.option(value=iforms.IKey(self.noneOption).key())[iforms.ILabel(self.noneOption).label()]
            if data is None:
                return
            for item in data:
                optValue = iforms.IKey(item).key()
                optLabel = iforms.ILabel(item).label()
                optValue = converter.fromType(optValue)
                option = T.option(value=optValue)[optLabel]
                if optValue == value:
                    option = option(selected='selected')
                yield option
            
        return T.select(name=key, id=keytocssid(ctx.key), data=self.options)[renderOptions]
        
    def processInput(self, ctx, key, args):
        value = args.get(key, [''])[0]
        value = iforms.IStringConvertible(self.original).toType(value)
        return self.original.validate(value)
        
        
class DatePartsInput(object):
    implements( iforms.IWidget )
    
    dayFirst = False
    
    def __init__(self, original, dayFirst=None):
        self.original = original
        if dayFirst is not None:
            self.dayFirst = dayFirst
            
    def _namer(self, prefix):
        def _(part):
            return '%s__%s' % (prefix,part)
        return _
            
    def render(self, ctx, key, args, errors):
        converter = iforms.IDateTupleConvertible(self.original)
        namer = self._namer(key)
        if errors:
            year = args.get(namer('year'), [''])[0]
            month = args.get(namer('month'), [''])[0]
            day = args.get(namer('day'), [''])[0]
        else:
            year, month, day = converter.fromType(args.get(key))
        yearTag = T.input(type="text", name=namer('year'), value=year, size=4)
        monthTag = T.input(type="text", name=namer('month'), value=month, size=2)
        dayTag = T.input(type="text", name=namer('day'), value=day, size=2)
        if self.dayFirst:
            return dayTag, ' / ', monthTag, ' / ', yearTag, ' (dd/mm/yyyy)'
        else:
            return monthTag, ' / ', dayTag, ' / ', yearTag, ' (mm/dd/yyyy)'
            
    def processInput(self, ctx, key, args):
        namer = self._namer(key)
        value = [args.get(namer(part), [''])[0].strip() for part in ('year', 'month', 'day')]
        value = [p for p in value if p]
        if not value:
            value = None
        elif len(value) != 3:
            raise validation.FieldValidationError("Invalid date")
        if value is not None:
            try:
                value = [int(p) for p in value]
            except ValueError, e:
                raise validation.FieldValidationError("Invalid date")
        value = iforms.IDateTupleConvertible(self.original).toType(value)
        return self.original.validate(value)


class MMYYDatePartsInput(object):
    implements( iforms.IWidget )
    
    cutoffYear = 70
    
    def __init__(self, original, cutoffYear=None):
        self.original = original
        if cutoffYear is not None:
            self.cutoffYear = cutoffYear
            
    def _namer(self, prefix):
        def _(part):
            return '%s__%s' % (prefix,part)
        return _
            
    def render(self, ctx, key, args, errors):
        converter = iforms.IDateTupleConvertible(self.original)
        namer = self._namer(key)
        if errors:
            year = args.get(namer('year'), [''])[0]
            month = args.get(namer('month'), [''])[0]
            # return a blank for the day
            day = ''
        else:
            year, month, day = converter.fromType(args.get(key))
            # if we have a year as default data, stringify it and only use last two digits
            if year is not None:
                year = str(year)[2:]
        yearTag = T.input(type="text", name=namer('year'), value=year, size=2)
        monthTag = T.input(type="text", name=namer('month'), value=month, size=2)
        return monthTag, ' / ', yearTag, ' (mm/yy)'
            
    def processInput(self, ctx, key, args):
        namer = self._namer(key)
        value = [args.get(namer(part), [''])[0].strip() for part in ('year', 'month')]
        value = [p for p in value if p]
        if not value:
            value = None
        elif len(value) != 2:
            raise validation.FieldValidationError("Invalid date")
        if value is not None:
            try:
                value = [int(p) for p in value]
            except ValueError, e:
                raise validation.FieldValidationError("Invalid date")
            if value[1] < 0 or value[1] > 99:
                raise validation.FieldValidationError("Invalid year. Please enter a two-digit year.")
            if value[0] > self.cutoffYear:
                value[0] = 1900 + value[0]
            else:
                value[0] = 2000 + value[0]
            value.append(1)
        value = iforms.IDateTupleConvertible(self.original).toType( value )
        return self.original.validate(value)
        
class CheckboxMultiChoice(object):
    implements( iforms.IWidget )
    
    options = None
    noneOption = ('', '')
    
    def __init__(self, original, options=None, noneOption=_UNSET):
        self.original = original
        if options is not None:
            self.options = options
        if noneOption is not _UNSET:
            self.noneOption = noneOption
    
    def render(self, ctx, key, args, errors):
        
        converter = iforms.IStringConvertible(self.original.type)
        
        if errors:
            values = args.get(key, [])
        else:
            values = args.get(key)
            if values is not None:
                values = [converter.fromType(v) for v in values]
            else:
                values = []
            
        # loops through checkbox options and renders 
        for n,item in enumerate(self.options):
            optValue = iforms.IKey(item).key()
            optLabel = iforms.ILabel(item).label()
            optValue = converter.fromType(optValue)
            optid = (keytocssid(ctx.key),'-',n)
            checkbox = T.input(type='checkbox', name=key, value=optValue, id=optid )
            if optValue in values:
                checkbox = checkbox(checked='checked')
            yield checkbox, T.label(for_=optid)[optLabel], T.br()
            
        
    def processInput(self, ctx, key, args):
        values = args.get(key, [])
        converter = iforms.IStringConvertible(self.original.type)
        values = [converter.toType(v) for v in values]
        return self.original.validate(values)


class FileUploadRaw(object):
    implements( iforms.IWidget )
    
    def __init__(self, original):
        self.original = original
        
    def render(self, ctx, key, args, errors):
        if errors:
            value = args.get(key, [''])[0]
        else:
            value = iforms.IFileConvertible(self.original).fromType(args.get(key))
        return T.input(name=key, id=keytocssid(ctx.key),type='file')
        
    def processInput(self, ctx, key, args):
        fileitem = inevow.IRequest(ctx).fields[key]
        name = fileitem.filename.decode(util.getPOSTCharset(ctx))
        value = (name, fileitem.file)

        value = iforms.IFileConvertible(self.original).fromType(value)
        return self.original.validate(value)


class FileUpload(object):
    implements( iforms.IWidget )
    
    def __init__(self, original, fileHandler, preview=None):
        self.original = original
        self.fileHandler = fileHandler
        self.preview = preview

    def _namer(self, prefix):
        def _(part):
            return '%s__%s' % (prefix,part)
        return _

    def render(self, ctx, key, args, errors):
        namer = self._namer(key)
        if errors:
            fileitem = inevow.IRequest(ctx).fields[key]
            name = fileitem.filename.decode(util.getPOSTCharset(ctx))
            if name:
                value = name
            else:
               namer = self._namer(key)
               value = args.get(namer('value'))[0]
        else:
            value = iforms.IStringConvertible(self.original).fromType(args.get(key))
            
        name = self.fileHandler.getUrlForFile(value)
        if name:
            if self.preview == 'image':
                yield T.p[value,T.img(src=self.fileHandler.getUrlForFile(value))]
            else:
                yield T.p[value]
        else:
            yield T.p[T.strong['nothing uploaded']]

        yield T.input(name=namer('value'),value=value,type='hidden')
        yield T.input(name=key, id=keytocssid(ctx.key),type='file')
        
    def processInput(self, ctx, key, args):
        fileitem = inevow.IRequest(ctx).fields[key]
        name = fileitem.filename.decode(util.getPOSTCharset(ctx))

        if name:
            value = self.fileHandler.storeFile( fileitem.file, name )
        else:
           namer = self._namer(key)
           value = args.get(namer('value'))[0]

        value = iforms.IStringConvertible(self.original).fromType(value)
        return self.original.validate(value)

class FileUploadWidget(object):
    implements( iforms.IWidget )

    FROM_RESOURCE_MANAGER = 'rm'
    FROM_CONVERTIBLE = 'cf'

    def _namer(self, prefix):
        def _(part):
            return '%s__%s' % (prefix,part)
        return _

    def __init__( self, original, convertibleFactory=None, originalKeyIsURL=False ): 
        self.original = original
        self.convertibleFactory = convertibleFactory()
        self.originalKeyIsURL = originalKeyIsURL

    def _blankField( self, field ):
        """
            Convert empty strings into None.
        """
        if field and field == '':
            return None
        return field
    
    def _getFromArgs( self, args, name ):
        """
            Get the first value of 'name' from 'args', or None.
        """
        rv = args.get( name )
        if rv:
            rv = rv[0]
        return rv

    def render(self, ctx, key, args, errors):
        """
            Render the data.

            This either renders a link to the original file, if specified, and
            no new file has been uploaded. Or a link to the uploaded file.

            The request to get the data should be routed to the getResouce 
            method.
        """
        form = iforms.IForm( ctx )

        namer = self._namer( key )
        resourceIdName = namer( 'resource_id' )
        originalIdName = namer( 'original_id' )

        # get the resource id first from the resource manager
        # then try the request
        resourceId = form.resourceManager.getResourceId( key )
        if resourceId is None:
            resourceId = self._getFromArgs( args, resourceIdName )
        resourceId = self._blankField( resourceId )

        # Get the original key from a hidden field in the request, 
        # then try the request file.data initial data.
        originalKey = self._getFromArgs( args, originalIdName )
        if not errors and not originalKey:
            originalKey = args.get( key )
        originalKey = self._blankField( originalKey )

        if errors:
            urlFactory = url.URL.fromContext( ctx ).sibling
        else:
            urlFactory = url.URL.fromContext( ctx ).child

        if resourceId:
            # Have an uploaded file, so render a URL to the uploaded file
            tmpURL = urlFactory(formWidgetResource(form.name)).child(key).child( self.FROM_RESOURCE_MANAGER ).child( resourceId )
            yield T.p[T.img(src=tmpURL)]
        elif originalKey:
            # The is no uploaded file, but there is an original, so render a
            # URL to it
            if self.originalKeyIsURL:
                tmpURL = originalKey
            else:
                tmpURL = urlFactory(formWidgetResource(form.name)).child(key).child( self.FROM_CONVERTIBLE ).child( originalKey )
            yield T.p[T.img(src=tmpURL)]
        else:
            # No uploaded file, no original
            yield T.p[T.strong['Nothing uploaded']]

        yield T.input(name=key, id=keytocssid(ctx.key),type='file')

        # Id of uploaded file in the resource manager
        yield T.input(name=resourceIdName,value=resourceId,type='hidden')
        if originalKey:
            # key of the original that can be used to get a file later
            yield T.input(name=originalIdName,value=originalKey,type='hidden')

    def processInput(self, ctx, key, args):
        """
            Process the request, storing any uploaded file in the 
            resource manager.
        """

        resourceManager = iforms.IForm( ctx ).resourceManager
    
        # Ping the resource manager with any resource ids that I know
        self._registerWithResourceManager( key, args, resourceManager ) 

        fileitem = inevow.IRequest(ctx).fields[key]
        name = fileitem.filename.decode(util.getPOSTCharset(ctx))
        if name:
            # Store the uploaded file in the resource manager
            resourceManager.setResource( key, fileitem.file, name )

        # Validating against an uploaded file. Should the fact that there is
        # original file meet a required field validation?
        return self.original.validate( resourceManager.getResourceForWidget( key ) )

    def _registerWithResourceManager( self, key, args, resourceManager ):
        """
            If there is a resource id in the request, then let the 
            resource manager know about it.
        """
        namer = self._namer( key )
        resourceIdName = namer( 'resource_id' )

        resourceId = self._getFromArgs( args, resourceIdName )
        resourceId = self._blankField( resourceId )
        if resourceId:
            resourceManager.register( key, resourceId )

    def getResource( self, ctx, segments ):
        """
            Return an Resource that contains the image, either a file
            from the resource manager, or a data object from the convertible.
        """

        if segments[0] == self.FROM_RESOURCE_MANAGER:
            # Resource manager can provide a path so return a static.File
            # instance that points to the file
            rm = iforms.IForm( ctx ).resourceManager
            (mimetype, path, fileName) = rm.getResourcePath( segments[1] )
            return static.File( path, mimetype ), []
        elif segments[0] == self.FROM_CONVERTIBLE:
            # The convertible can provide a file like object so create a
            # static.Data instance with the data from the convertible.

            def _( result ):
                mimetype, filelike, fileName = result
                data = filelike.read()
                filelike.close()
                return static.Data( data, mimetype ), []

            d = defer.maybeDeferred( self.convertibleFactory.fromType, segments[1], context=ctx )
            d.addCallback( _ )
            return d
        else:
            return None

class Hidden(object):
    __implements__ = iforms.IWidget,

    hidden = True
    inputType = 'hidden'

    def __init__(self, original):
        self.original = original

    def render(self, ctx, key, args, errors):
        if errors:
            value = args.get(key, [''])[0]
        else:
            value = iforms.IStringConvertible(self.original).fromType(args.get(key))
        return T.input(type=self.inputType, name=key, id=keytocssid(ctx.key), value=value)

    def processInput(self, ctx, key, args):
        value = args.get(key, [''])[0].decode(util.getPOSTCharset(ctx))
        value = iforms.IStringConvertible(self.original).toType(value)
        return self.original.validate(value)

__all__ = [
    'Checkbox', 'CheckboxMultiChoice', 'CheckedPassword','FileUploadRaw', 'FileUpload', 'FileUploadWidget',
    'Password', 'SelectChoice', 'TextArea', 'TextInput', 'DatePartsInput',
    'MMYYDatePartsInput', 'Hidden'
    ]
    
