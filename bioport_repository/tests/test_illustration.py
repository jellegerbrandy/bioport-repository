#!/usr/bin/env python
#encoding=utf8

import os
import urllib2
import unittest
from cStringIO import StringIO
import shutil

import PIL.Image

from bioport_repository.tests.common_testcase import CommonTestCase, IMAGES_CACHE_LOCAL
from bioport_repository.illustration import Illustration


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
url_root = 'file://%s/data/images' % THIS_DIR
images = '%s/data/images' % THIS_DIR
images_cache_local = IMAGES_CACHE_LOCAL 
images_cache_url = 'file://%s' % IMAGES_CACHE_LOCAL 
fn = 'image1.jpg'
fn2 = u'im\xebge.jpg'


class IllustrationTestCase(CommonTestCase):

    def setUp(self): 
        CommonTestCase.setUp(self)
        #fn2 has a unicode name, which trips up svn, so we copy it and later remove it
        shutil.copyfile(os.path.join(images, fn), os.path.join(images, fn2))

    def test_create_id(self):
        ill = Illustration('xxx', None, None)
        assert ill.create_id().endswith('xxx')
        ill = Illustration('xxx?asdf=xfajl&adsfklj=x', None, None)
        ill2 = Illustration('xxx?asdf=aaa&adsfklj=x', None, None)
        assert ill.create_id().endswith('xxx')
        self.assertNotEqual(ill.create_id(), ill2.create_id())
        
    def test_illustration_standalone(self):
        ill = Illustration(
            url=os.path.join(url_root ,fn), 
            images_cache_local=images_cache_local,
            images_cache_url =images_cache_url,
            prefix = 'test',
            )
        ill.download()
        local_fn =  ill.cached_local
        self.failUnless(os.path.exists(local_fn))
        self.failUnless(urllib2.urlopen(ill.cached_url).read())
        
        
        ill = Illustration(
            url=os.path.join(url_root ,fn2), 
            images_cache_local=images_cache_local,
            images_cache_url =images_cache_url,
            prefix = 'test'
            )
        ill.download()
        image_path = ill.cached_local
        self.failUnless(os.path.exists(image_path))
        self.failUnless(os.listdir(images_cache_local))
        image_url = ill.cached_url
        image_contents = urllib2.urlopen(image_url).read()      
        self.failUnless(image_contents)
        
    def test_illustration_in_repository(self):
        repo = self.repo
        repo.images_cache_local = images_cache_local
        repo.images_cache_url = images_cache_url
        source = repo.get_sources()[0]
        
        [repo.download_illustrations(s) for s in repo.get_sources()]
        for person in [p for p in repo.get_persons()
                        if p.has_illustrations]:
            for biography  in person.get_biographies():
                for illustration in biography.get_illustrations():
                    #should have downloaded this image
                    illustration.download()
 
                    self.failUnless(os.path.exists(illustration.cached_local))
                    url = illustration.cached_url
                    self.failUnless(urllib2.urlopen(url).read())
                    path = illustration.cached_local
                    self.failUnless(os.path.exists(path))

    def test_illustration_with_same_name_as_another(self):
        repo = self.repo
        repo.images_cache_local = images_cache_local
        repo.images_cache_url = images_cache_url
        [repo.download_illustrations(s) for s in repo.get_sources()]
        illustrations = []
        for person in [p for p in repo.get_persons()
                        if p.has_illustrations]:
            for biography  in person.get_biographies():
                for illustration in biography.get_illustrations():
                    illustrations.append(illustration)
        illustration_paths = [a.cached_local for a in illustrations]


class ThumbnailTestCase(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(images_cache_local):
            os.mkdir(images_cache_local)
        super(ThumbnailTestCase, self).setUp()
        self.ill = Illustration(
            url=os.path.join(url_root ,fn), 
            images_cache_local=images_cache_local,
            images_cache_url =images_cache_url,
            prefix = 'test'
            )

    def test_thumbnail_generation(self):
        ill = self.ill
#        self.failIf(ill.has_thumbnail(width=50, height=50))
        ill.create_thumbnail(width=50, height=50)
        self.failUnless(ill.has_thumbnail(width=50, height=50))
        thumbnail_url = ill.thumbnail_url(width=50, height=50)
        thumbnail_data = urllib2.urlopen(thumbnail_url).read()
        img = PIL.Image.open(StringIO(thumbnail_data))
        self.failUnless(img.size[0]==50 or img.size[1]==50)

    def test_on_demand_thumbnail_generation(self):
        ill = self.ill
        thumbnail_url = ill.thumbnail_url(width=50, height=50)
        thumbnail_data = urllib2.urlopen(thumbnail_url).read()
        img = PIL.Image.open(StringIO(thumbnail_data))
        self.failUnless(img.size[0]==50 or img.size[1]==50)

if __name__ == "__main__":
    unittest.main(defaultTest='IllustrationTestCase.test_illustration_in_repository')
    unittest.main()
    

