"""
Widgets are small components that render form fields for inputing data in a
certain format.
"""

import mimetypes
from nevow import inevow, rend, tags as T, util
from forms import iforms, types, validation
from forms.util import keytocssid

# Marker object for args that are not supplied
_UNSET = object()
        
        
class TextInput(object):
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
        
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
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
    
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
    __implements__ = iforms.IWidget,
    
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
            
        if value is not None:
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


__all__ = [
    'Checkbox', 'CheckboxMultiChoice', 'CheckedPassword','FileUploadRaw', 'FileUpload',
    'Password', 'SelectChoice', 'TextArea', 'TextInput', 'DatePartsInput',
    'MMYYDatePartsInput',
    ]
    
