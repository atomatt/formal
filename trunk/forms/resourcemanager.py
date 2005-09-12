import tempfile
import mimetypes
import re
import os
from shutil import copyfileobj
from exceptions import IOError, OSError


class ResourceManagerException( Exception ):
    def __init__( self, *args, **kwds ):
        super( ResourceManagerException, self ).__init__( *args, **kwds )

class ResourceManager( object ):
    def __init__( self ):
        self.widgetToID = {}

    def register( self, widgetName, resourceId ):
        self.widgetToID[widgetName] = resourceId

    def getResourceId( self, widgetName ):
        return self.widgetToID.get( widgetName )

    def getResourceForWidget( self, widgetName ):
        resourceId = self.getResourceId( widgetName )
        if resourceId is None:
            return None
        (path, fileName) = self._fromResourceId( resourceId )
        mimetype = mimetypes.guess_type( fileName )[0]
        try:
            filelike = open( path, 'r' )
            return (mimetype, filelike, fileName)
        except IOError:
            return None

    def getResourcePath( self, resourceId ):
        """
            Required to create an instance of nevow.static.File
        """
        (path, fileName) = self._fromResourceId( resourceId )
        mimetype = mimetypes.guess_type( fileName )[0]
        return (mimetype, path, fileName)

    def setResource( self, widgetName, filelike, fileName ):
        existingResource = self.widgetToID.get( widgetName )
        if existingResource is not None:
            try:
                (path, ignore) = self._fromResourceId( existingResource )
                os.remove( path )
            except OSError:
                pass

        fileName = fileName.replace( '_', '-' )

        (target, path) = tempfile.mkstemp( '__' + fileName )
        
        # target is a file handle so reopen it as a file instance.
        os.close( target )
        target = open( path, 'w' )
        
        copyfileobj( filelike, target )
        target.close()
        resourceId = self._toResourceId( path )
        self.widgetToID[widgetName] = resourceId
        return resourceId

    def _fromResourceId( self, resourceId ):
        match = re.match( '^.*__(.*)$', resourceId )
        if match is None:
            return None
        fileName = match.group( 1 )
        path = os.sep.join( (tempfile.gettempdir(), resourceId) )
        return path, fileName

    def _toResourceId( self, path ):
        path = path[len(tempfile.gettempdir()):]
        if path[0] == os.sep:
            path = path[1:]
        return path

    def clearUpResources( self ):
        for id in self.widgetToID.values():
            try:
                (path, fileName) = self._fromResourceId( id )
                os.remove( path )
            except OSError:
                pass
        
