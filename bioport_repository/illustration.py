#!/usr/bin/env python

from __future__ import with_statement

import os
import urllib2
import traceback
import sys
from hashlib import md5
import simplejson

from zLOG import LOG, INFO, ERROR, WARNING
import PIL.Image
from cStringIO import StringIO


MEDIUM_THUMB_SIZE = (200, 200)
SMALL_THUMB_SIZE = (100, 100)

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 120

def get_digest(astring):
    return md5(astring).hexdigest()

def logexception():
    msg = traceback.format_exc()
    print >>sys.stderr
    LOG('BioPort', ERROR, msg)


class Illustration:
    """XXX - needs docstring"""

    def __init__(self, url, 
                       images_cache_local,
                       images_cache_url,
                       prefix = '',
                       caption=None,
                       link_url=None): 
        """
        arguments:
           url  : the original url of the image
           images_cache_local : path to a place on the filesystem where the image will be downloaded to
           images_cache_url : url at which the image will be accessabiel once downloaded
           link_url: an optional url to link to
           prefix : will be prefixed to the local cached filename 
        """
        self._url = url
        self._images_cache_local = images_cache_local  or ''  # XXX it should be renamed in _images_directory
        self._thumbnails_directory = os.path.join(self._images_cache_local, 'thumbnails')
        if not os.path.isdir(self._thumbnails_directory):
            os.mkdir(self._thumbnails_directory)
        self._images_cache_url = images_cache_url  or ''
        self._prefix = prefix
        self._link_url = link_url
        self._caption = caption


    # --- public API used by the view

    @property
    def link_url(self):
        """The url of the site the biography points to"""
        return self._link_url

    @property
    def caption(self):
        return self._caption
        
    @property
    def json_stripped_caption(self):
        return simplejson.dumps(self.caption)

    @property
    def original_image_url(self):
        pass

    # --- public API used *internally* (not by the view) 

    @property
    def source_url(self):
        """the original url of the image (typically on an external sever)"""
        return self._url

    @property
    def images_directory(self):
        """The physical path on disk where the images are held/saved"""
        return self._images_cache_local

    @property
    def thumbnails_directory(self):
        """The physical path on disk where the thumbnails are held/saved"""
        return self._thumbnails_directory
        
    @property          
    def cached_local(self):
        """path on the local file system to a copy of the image"""
        return os.path.join(self._images_cache_local,  self.create_id())
    
    @property
    def cached_url(self):
        """public url of the local copy of the image"""
        return os.path.join(self._images_cache_url, self.create_id())

    def cached_thumbnail_local(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        return os.path.join(self._images_cache_local,  'thumbnails', '%ix%i_%s'
                            % (width, height, self.create_id()))
        
    def thumbnail_url(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        """public url of the thumbnail of this image
        If the thumbnail doesn't exist yet it wil be generated
        """
        if not self.has_thumbnail(width,height):
            return ""
            # XXX
#            try:
#	            self.create_thumbnail(width,height, refresh=True)
#            except IOError: 
                # probably because we cannot find the original file either
                # we let this go, because we do not want the whole page to throw an error
                # because of a broken link
#                logexception()                
        return "/".join((self._images_cache_url, 'thumbnails', '%ix%i_%s'
                        % (width, height, self.create_id())))

    def download(self, overwrite=True):
        """Download the original image with original dimensions and saves it on
        disk.

        Also, create two resized images which will then by used in the view,
        a medium and a smaller one, which will be saved im /thumbnails directory
        """
        if not overwrite and os.path.exists(self.cached_local):
            print 'XXX - image already exists at %s - no image downloaded' % self.cached_local
            return

        url = self.source_url
        LOG('BioPort', INFO, 'downloading image from %s to %s' % (repr(url), repr(self.cached_local)))

        #  XXX - temporary
        """    
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
        """

        # write main image file on disk
        http = urllib2.urlopen(url)
        with open(self.cached_local, 'w') as file:
            file.write(http.read())

        # wirte two smaller thumbs on disk
        self._create_thumbnail(*MEDIUM_THUMB_SIZE)
        self._create_thumbnail(*SMALL_THUMB_SIZE)

    def _create_thumbnail(self, width, height):
        """
        Create a thumbnail of the image and store a local copy
        width and height are sizes in pixels - the image should fit within
        the rectangle defined by these sizes.
        inspired from Products.Archetypes.Field
        """
        assert isinstance(width, int)
        assert isinstance(height, int)       
        if not os.path.isfile(self.cached_local): 
              raise("the original image does not exists (it was supposed to be found here: %s)" 
                     % self.cached_local)

        # PIL stuff
        pilfilter = 0  # NEAREST
        if PIL.Image.VERSION >= "1.1.3":
            pilfilter = 1  # ANTIALIAS
        image = PIL.Image.open(self.cached_local)
        image = image.convert('RGB')
        image.thumbnail((width, height), pilfilter)

        # write on disk
        basename = os.path.basename(self.cached_local)
        basename = "%sx%s_%s" % (width, height, basename)
        file = os.path.join(self.thumbnails_directory, basename)
        image.save(file, "JPEG", quality=88) 

    def has_thumbnail(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        return os.path.isfile(self.cached_thumbnail_local(width, height))
    
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


