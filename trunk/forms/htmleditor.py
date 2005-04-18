from nevow import tags as T
from forms import iforms


tinyMCEGlue = T.xml("""
    <!-- tinyMCE -->
    <script language="javascript" type="text/javascript" src="/tiny_mce/tiny_mce.js"></script>
    <script language="javascript" type="text/javascript">
       tinyMCE.init({
          mode : "specific_textareas"
          theme: 'advanced',
          theme_advanced_toolbar_location: 'top',
          theme_advanced_toolbar_align: 'left'
       });
    </script>
    <!-- /tinyMCE -->
    """ )
    

class TinyMCE(object):
    __implements__ = iforms.IWidget,
    
    def __init__(self, original):
        self.original = original
    
    def render(self, ctx, key, args, errors):
        if errors:
            value = args.get(key, [''])[0]
        else:
            value = iforms.IStringConvertible(self.original).fromType(args.get(key))
        return T.textarea(name=key, id=key, mce_editable='true')[value or '']
        
    def processInput(self, ctx, key, args):
        value = args.get(key, [''])[0]
        value = iforms.IStringConvertible(self.original).toType(value)
        return self.original.validate(value)

