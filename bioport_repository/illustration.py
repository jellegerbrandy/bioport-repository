#!/usr/bin/env python

import os
import urllib2
from hashlib import md5

import PIL.Image
from cStringIO import StringIO
from zLOG import WARNING, LOG, INFO

DEFAULT_WIDTH = 120
DEFAULT_HEIGHT = 100


class Illustration:
    """XXX - needs docstring"""

    def __init__(self,
        url, 
        images_cache_local,
        images_cache_url,
        prefix = '',
        caption=None,
        link_url=None,
        ): 
        """
        arguments:
           url  : the original url of the image
           images_cache_local : path to a place on the filesystem where the image will be downloaded to
           images_cache_url : url at which the image will be accessabiel once downloaded
           link_url: an optional url to link to
           prefix : will be prefixed to the local cached filename 
        """
        self._url = url
        self._images_cache_local = images_cache_local  or ''
        self._images_cache_url = images_cache_url  or ''
        self._prefix = prefix
        self._link_url = link_url
        self.caption = caption
        
    def create_id(self):
        url = self._url
        filename = url.split('/')[-1]
        #create a unique hash on the basis of the url
        #(the hash code is created in this somewhat illogical way to maintian compatibility with earlier versions)
        url_to_hash = '/'.join(url.split('/')[:-1])
        if '?' in url:
            url_to_hash=url
        digest = get_digest(url_to_hash)
        filename = filename.split('?')[0]
        filename = '%s_%s_%s' % (self._prefix, digest, filename)
        return filename
    
    def source_url(self):
        """the original url of the image (typically on an external sever)"""
        return self._url
    def cached_local(self):
        """path on the local file system to a copy of the image"""
        return os.path.join(self._images_cache_local,  self.create_id())
    
    def cached_url(self):
        """public url of the local copy of the image"""
        return os.path.join(self._images_cache_url, self.create_id())

    def link_url(self):
        return self._link_url
        
    def download(self, refresh=True):
        if not refresh and os.path.exists(self.cached_local()):
            #print 'image already exists at %s - no image downloaded' % self.cached_local()
            return
        url = self._url
#        url = url[:len('http://'):] + urllib2.quote(url[len('http://'):].encode('utf8'))
#        url  =self._url.encode('utf8')
#        import pdb; pdb.set_trace()
        try:
            msg = 'downloading image at %s to %s' % (url, self.cached_local())
        except:
            LOG('BioPort', INFO, 'donwloading image - filename could ot be printed')
        else:
            LOG('BioPort', INFO, msg)
            
        try:
            f = urllib2.urlopen(url)
        except (urllib2.HTTPError, OSError):
            url = url.encode('latin1')
            url = url.replace(' ', '%20')
            try:
                f = urllib2.urlopen(url)
            except (urllib2.HTTPError, OSError), error:
                msg= 'WARNING: error downloading %s [%s]' % (repr(url), error)
                LOG('BioPort', WARNING, msg)
                return
        except UnicodeEncodeError: 
            url = url.encode('latin1')
            url = url.replace(' ', '%20')
            try:
                f = urllib2.urlopen(url)
            except (urllib2.HTTPError, OSError), error:
                msg= 'WARNING: error downloading %s [%s]' % (repr(url), error)
                LOG('BioPort', WARNING, msg)
                return 
        
        fh = open(self.cached_local(), 'w')
        fh.write(f.read())
        fh.close()

    def create_thumbnail(self,
                         width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                         refresh=False):
        """ create a thumbnail of the image and store a local copy
            width and height are sizes in pixels - the image should fit within
            the rectangle defined by these sizes.
            inspired from Products.Archetypes.Field"""
        #make sure we have valid int's
        keys = {'height':int(height), 'width':int(width)}
        if not refresh and self.has_thumbnail(keys['width'],keys['height']):
            return 
        # download the image if it doesn't exist
        if not os.path.isfile(self.cached_local()):
            self.download()
        pilfilter = 0 # NEAREST
        #check for the pil version and enable antialias if > 1.1.3
        if PIL.Image.VERSION >= "1.1.3":
            pilfilter = 1 # ANTIALIAS

        image = PIL.Image.open(self.cached_local())
        image = image.convert('RGB')
        image.thumbnail((keys['width'],keys['height']), pilfilter)
        thumbnail_file = StringIO()
        image.save(thumbnail_file, "JPEG", quality=88)
        self._store_thumbnail(keys['width'],keys['height'], thumbnail_file.getvalue())

    def has_thumbnail(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        return os.path.isfile(self.cached_thumbnail_local(width, height))
    
    def _store_thumbnail(self, width, height, data):
        try:
            fh = open(self.cached_thumbnail_local(width, height), 'w')
        except IOError, error:
            try:
	            os.mkdir("/".join((self._images_cache_local, 'thumbnails')))
	            fh = open(self.cached_thumbnail_local(width, height), 'w')
            except OSError, error:
                #XXX LOG error
                return
            
        fh.write(data)
        fh.close()

    def thumbnail_url(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        """public url of the thumbnail of this image
           If the thumbnail doesn't exist yet it wil be generated"""
        if not self.has_thumbnail(width,height):
            try:
	            self.create_thumbnail(width,height, refresh=True)
            except IOError: #probably because we cannot find the original file either
                #we let this go, because we do not want the whole page to throw an error
                #because of a broken link
                pass
        return "/".join((self._images_cache_url, 'thumbnails', '%ix%i_%s'
                        % (width, height, self.create_id()) ))
    def cached_thumbnail_local(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        return os.path.join(self._images_cache_local,  'thumbnails', '%ix%i_%s'
                            % (width, height, self.create_id()))
                            

def get_digest(astring):
    return md5(astring).hexdigest()

