import os
from shutil import copyfileobj

FILESTORE_DIR='assets'
FILESTORE_URL='webassets'

class fileResource:
    
    def getUrlForFile(self, id):
        if id:
            return os.path.join(FILESTORE_URL, id)
        else:
            return None
    def storeFile( self, source, name ):
        id = name
        target = file(os.path.join(FILESTORE_DIR,id),'w')
        copyfileobj( source, target )
        target.close()
        return id