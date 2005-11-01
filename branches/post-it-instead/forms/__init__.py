"""A package (for Nevow) for defining the schema, validation and rendering of
HTML forms.
"""


version_info = (0, 3, 0)
version = '.'.join([str(i) for i in version_info])


from nevow import static

from forms.types import *
from forms.validation import *
from forms.widget import *
from forms.form import Form, ResourceMixin, renderForm
from forms import iforms

def widgetFactory(widgetClass, *a, **k):
    def _(original):
        return widgetClass(original, *a, **k)
    return _

try:
    import pkg_resources
except ImportError:
    import os.path
    defaultCSS = static.File(os.path.join(os.path.split(__file__)[0], 'forms.css'))
else:
    defaultCSS = static.File(pkg_resources.resource_filename('forms', 'forms.css'))

# Register standard adapters
from nevow.compy import registerAdapter
from forms import converters
registerAdapter(TextInput, String, iforms.IWidget)
registerAdapter(TextInput, Integer, iforms.IWidget)
registerAdapter(TextInput, Float, iforms.IWidget)
registerAdapter(Checkbox, Boolean, iforms.IWidget)
registerAdapter(DatePartsInput, Date, iforms.IWidget)
registerAdapter(TextInput, Time, iforms.IWidget)
registerAdapter(FileUploadRaw, File, iforms.IWidget)
from forms import util
registerAdapter(util.SequenceKeyLabelAdapter, tuple, iforms.IKey)
registerAdapter(util.SequenceKeyLabelAdapter, tuple, iforms.ILabel)
registerAdapter(converters.NullConverter, String, iforms.IStringConvertible)
registerAdapter(converters.DateToDateTupleConverter, Date, iforms.IDateTupleConvertible)
registerAdapter(converters.BooleanToStringConverter, Boolean, iforms.IBooleanConvertible)
registerAdapter(converters.IntegerToStringConverter, Integer, iforms.IStringConvertible)
registerAdapter(converters.FloatToStringConverter, Float, iforms.IStringConvertible)
registerAdapter(converters.DateToStringConverter, Date, iforms.IStringConvertible)
registerAdapter(converters.TimeToStringConverter, Time, iforms.IStringConvertible)
registerAdapter(converters.NullConverter, File, iforms.IFileConvertible)
registerAdapter(converters.NullConverter, Sequence, iforms.ISequenceConvertible)
del registerAdapter

