import os

import numpy as np

from fs.opener import opener, fsopen
from fs.errors import FSError

from traits.api import HasTraits, Str, Unicode, Trait, TraitHandler, Property

import logging
log = logging.getLogger(__name__)


def normalize_uri(uri):
    if uri.startswith("file://"):
        # FIXME: workaround to allow opening of file:// URLs with the
        # ! character
        uri = uri.replace("file://", "")
    if uri:
        fs, relpath = opener.parse(uri)
        if fs.haspathurl(relpath):
            uri = fs.getpathurl(relpath)
        elif fs.hassyspath(relpath):
            abspath = fs.getsyspath(relpath)
            if abspath.startswith("\\\\?\\UNC\\"):
                # Leave long UNC paths as raw paths because there is no
                # accepted way to convert to URI
                uri = abspath
            else:
                if abspath.startswith("\\\\?\\") and len(abspath) < 260:
                    # on windows, pyfilesystem returns extended path notation to
                    # allow paths greater than 256 characters.  If the path is
                    # short, change slashes to normal and remove the prefix
                    abspath = abspath[4:].replace("\\", "/")
                uri = "file://" + abspath
    return uri


class TraitUriNormalizer(TraitHandler):
    """Trait validator to convert bytes to numpy array"""
    def validate(self, object, name, value):
        try:
            uri = normalize_uri(value)
            return uri
        except FSError:
            # Allow the error to be caught when the file is actually opened
            return value
        except:
            self.error(object, name, value)

    def info(self):
        return '**a string or unicode URI**'


class FileMetadata(HasTraits):
    uri = Trait("", TraitUriNormalizer())
    
    mime = Str(default="application/octet-stream")
    
    name = Property(Unicode, depends_on='uri')
    
    def __str__(self):
        return "uri=%s, mime=%s" % (self.uri, self.mime)

    def _get_name(self):
        return os.path.basename(self.uri)


class FileGuess(object):
    """Loads the first part of a file and provides a container for metadata

    """
    # Arbitrary size header, but should be large enough that binary files can
    # be scanned for a signature
    head_size = 1024*1024
    
    def __init__(self, uri):
        log.debug("Attempting to load %s" % uri)
        self.reload(uri)
    
    def reload(self, uri=None):
        if uri is None:
            uri = self.metadata.uri
        if uri.startswith("file://"):
            # FIXME: workaround to allow opening of file:// URLs with the
            # ! character
            uri = uri.replace("file://", "")
        fs, relpath = opener.parse(uri)
        log.debug("Filesystem: %s" % fs)
        fh = fs.open(relpath, "rb")
        
        # In order to handle arbitrarily sized files, only read the first
        # header bytes.  If the file is bigger, it will be read by the task
        # as needed.
        self._numpy = None
        self.bytes = fh.read(self.head_size)
        fh.close()
        
        # Use the default mime type until it is recognized
        self.metadata = FileMetadata(uri=uri)
        
        # Release filesystem resources
        fs.close()
        
    def __str__(self):
        return "guess: metadata: %s, %d bytes available for signature" % (self.metadata, len(self.bytes))
    
    def get_utf8(self):
        return self.bytes
    
    @property
    def numpy(self):
        if self._numpy is None:
            self._numpy = np.fromstring(self.bytes, dtype=np.uint8)
        return self._numpy
    
    def get_metadata(self):
        return self.metadata.clone_traits()

    def get_stream(self):
        fs, relpath = opener.parse(self.metadata.uri)
        fh = fs.open(relpath, "rb")
        return fh
