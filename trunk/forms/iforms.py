from nevow.compy import Interface


class IType(Interface):
    def validate(self, value):
        pass

        
class IStructure(Interface):
    pass
    
    
class IWidget(Interface):
    
    def render(self, ctx, key, args, errors):
        pass
    
    def processInput(self, ctx, key, args):
        pass


class IFormFactory(Interface):
    def formFactory(self, ctx, name):
        pass
        
        
class IFormData(Interface):
    pass
    
    
class IFormErrors(Interface):
    pass
    
    
class IKey(Interface):
    def key(self):
        pass

        
class ILabel(Interface):
    def label(self):
        pass

        
class IConvertible(Interface):
    def fromType(self, value):
        pass
    def toType(self, value):
        pass
    
        
class IStringConvertible(IConvertible):
    pass
    
    
class IBooleanConvertible(IConvertible):
    pass
    
    
class IDateTupleConvertible(IConvertible):
    pass

    
class IFileConvertible(IConvertible):
    pass
    
