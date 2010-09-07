#!/usr/bin/env python

"""This package handles the data reposotiry for Bioport."""

import os
import time
import urllib2
import logging

from plone.memoize import instance
from lxml import etree
from sqlalchemy.exceptions import IntegrityError, InvalidRequestError
import biodes

from bioport_repository.db_definitions import STATUS_NEW, STATUS_VALUES
from bioport_repository.biography import Biography
from bioport_repository.db import DBRepository
from bioport_repository.local_settings import *
from bioport_repository.person import Person
from bioport_repository.repocommon import BioPortException
from bioport_repository.source import BioPortSource, Source
from bioport_repository.svn_repository import SVNRepository
from bioport_repository.illustration import CantDownloadImage


class Repository(object):
    #__metaclass__ = Singleton
    
    ENABLE_SVN = False
    ENABLE_DB = True

    def __init__(self, 
        svn_repository=None,
        svn_repository_local_copy=None,
        db_connection=None,
        ZOPE_SESSIONS = False,
        user='Uknown User',
        images_cache_local=None,
        images_cache_url=None,
        ):
        
        #define the database connection
        self.svn_repository = SVNRepository(svn_repository=svn_repository, svn_repository_local_copy=svn_repository_local_copy)
        self.db = DBRepository(db_connection=db_connection, ZOPE_SESSIONS=ZOPE_SESSIONS, user=user)
        self.db.repository = self
        
        if images_cache_local:
            assert os.path.exists(images_cache_local), 'this path (for "images_local_cache") does not exist; %s'% images_cache_local
        self.images_cache_local = images_cache_local
        self.images_cache_url = images_cache_url
        self.user=user
        
    def commit(self, svn_entry=None):
        """commmit the local changes to the resository"""
        if self.ENABLE_SVN:
            #XXX put some useful message here
            msg = 'put some useful message here'
            if svn_entry:
                self.svn_repository.commit(msg, svn_entry.path())
            else:
                self.svn_repository.commit(msg)
        
    def get_bioport_ids(self):
        return self.db.get_bioport_ids()
            
    def get_person(self, bioport_id):
        return self.db.get_person(bioport_id=bioport_id)
        
    def count_persons(self, **args):
        return self.db.count_persons(**args)

    def get_persons(self, **args): 
        """Get for all persons (as opposed to biographies)
        
        arguments:
            order_by - a string - default is 'sort_key'
            XXX: arguments for selecting persons
        
        returns: a list of Person instances
        """
        #XXX of course, we need to get this from the cache
        #and if we do, we can move this code to svn_repository
        if self.ENABLE_DB:
            return self.db.get_persons(**args)
        elif self.ENABLE_SVN:
            raise NotImplementedError()

    def get_persons_sequence(self, **args):
        "this method is like get_persons, but defers Person instantiation"
        qry = self.db._get_persons_query(**args)
        return PersonList(qry, self)

    def delete_person(self, person):
        if self.ENABLE_DB:
            return self.db.delete_person(person)
        if self.ENABLE_SVN:
            raise NotImplementedError()
    
    def count_biographies(self, **args):
        return self.db.count_biographies(**args)
    def get_biographies(self, **args):
            
        if self.ENABLE_DB:
            return self.db.get_biographies(**args)
        elif self.ENABLE_SVN:
            raise NotImplementedError()
        
        
    def get_biography(self, local_id=None, **args):
        return self.db.get_biography(local_id=local_id, **args)
    
    def redirects_to(self, bioport_id):
        return self.db.redirects_to(bioport_id)
        
        
    @instance.clearafter
    def add_source(self, source):
        """add a source of data to the db"""
        if source.id in [src.id for src in self.get_sources()]:
            raise ValueError('A source with id %s already exists' % source.id)
        if self.ENABLE_DB:
            self.db.add_source(source)
        if self.ENABLE_SVN:
            self.svn_repository.add_source(source)
        self.invalidate_cache('_sources')
        return source        
    
    @instance.clearafter
    def delete_source(self, source):
        if self.ENABLE_DB:
            self.db.delete_source(source)
            
        if self.ENABLE_SVN:
            self.svn_repository.delete_source(source)
            
  
    @instance.memoize
    def get_source(self, id):
        ls = [src for src in self.get_sources() if src.id == id]
        if not ls:
            raise ValueError('No source found with id %s\nAvailabe sources are %s' % (id, [s.id for s in self.get_sources()]))
        return ls[0]
     
    @instance.memoize
    def get_sources(self, order_by='quality', desc=True):
        """
        return:
            a list of Source instances
        """
        if self.ENABLE_DB:
            self._sources = self.db.get_sources(order_by=order_by, desc=desc)
        elif self.ENABLE_SVN:
            self._sources = self.svn_repository.get_sources(order_by=order_by, desc=desc)
        return self._sources
   
    def get_status_values(self, k=None):
        items = STATUS_VALUES
        if k:
            return dict(items)[k]
        else:
            return items
    def get_authors(self, **args):
        if self.ENABLE_DB:
            return self.db.get_authors(**args)
        raise NotImplementedError 

    def get_author(self, author_id):
        if self.ENABLE_DB:
            return self.db.get_author(author_id)
        raise NotImplementedError 
    def get_beroepen(self, **args):
        pass
    def save(self, x):
        if x.__class__ == Biography:
            self.save_biography(x)
        elif x.__class__ == Source:
            self.save_source(x)
        else:
            raise TypeError('Cannot save a object %s in the repository: unknown type' % x)
    def save_biography(self, biography):
        biography.repository = self
        if self.ENABLE_DB:
            self.db.save_biography(biography)
        if self.ENABLE_SVN:
            raise NotImplementedError()

        biography.get_person().invalidate_cache('_biographies')
    
    @instance.clearafter 
    def save_source(self, source):
        source.repository = self
        self.invalidate_cache('_sources')
        if self.ENABLE_DB:
            self.db.save_source(source)
        if self.ENABLE_SVN:
            raise NotImplementedError()
    
    def save_person(self, person):
        if self.ENABLE_DB:
            self.db.save_person(person)
        if self.ENABLE_SVN:
            raise NotImplementedError()
        
    
    def delete_biographies(self, source):
	sources_ids = [src.id for src in self.get_sources()]
	if source.id not in sources_ids:
	    raise ValueError("no source with id %s was found" % source.id)
        if self.ENABLE_DB:
            self.db.delete_biographies(source)
        if self.ENABLE_SVN:
            raise NotImplementedError
    
    def download_biographies(self, source, limit=None, sleep=0):
        """Download all biographies from source.url and add them to the repository.
        Mark any biographies that we did not find (anymore), by removing the source_url property.
        Return the number of total and skipped biographies.
       
        arguments:    
            source: a Source instance
        
        returns:
             a list of biography instances
             XXX: this should perhaps be in iteraor?
        """
        
        #at the URL given we find a list of links to biodes files
        #print 'Opening', source.url
        assert source.url, 'No URL was defined with the source "%s"' % source.id
        
        logging.info('downloading data at %s' % source.url)
        try:
            ls = biodes.parse_list(source.url)
            if limit:
                ls = ls[:limit] 
        except etree.XMLSyntaxError, error:
            raise BioPortException('Error parsing data at %s -- check if this is valid XML\n%s' % (source.url, error))
        
        logging.info('done parsing source url')
        #the data seems ok; we now delete all biographies (!)
#        print 'Deleting all biographies from source %s' % source.id
#        self.delete_biographies(source=source)
        
        
        i = 0
        if not ls:
            raise BioPortException('The list at %s does not contain any links to biographies' % source.url)

        total = len(ls)
        skipped = 0
        for biourl in ls:
            if not biourl.startswith("http:"):
                # we're dealing with a fs path
                biourl = os.path.normpath(biourl)
                if not os.path.isabs(biourl):
                    biourl = os.path.join(os.path.dirname(source.url), biourl)

            i += 1
            if limit and i > limit:
                break
            logging.info('progress %s/%s: adding biography at %s' %(i, len(ls), biourl))
            #we download each o fthe documents
            #local_id = os.path.splitext(os.path.split(biourl)[1])[0]
            
            #create a Biography object 
            bio = Biography(source_id=source.id, repository=source.repository)
            if sleep:
                time.sleep(sleep)  
            try:
                bio.from_url(biourl)
            except Exception, error:
                msg = 'Problems downloading biography from %s:\n%s' % (biourl, error)
                logging.warning( msg)
                continue
            try:
                self.add_biography(bio)
            except Exception, error:
                skipped += 1
                logging.warning( 'Problems adding biography from %s:\n%s' % (biourl, error))
                raise
            

        s = '%s biographies downloaded from source %s' % (i, source.id)
        self.delete_orphaned_persons(source_id=source.id)
        return total, skipped
    
    def delete_orphaned_persons(self, **args):
        #remove all elements from the person table that do not have any biographies associated with them anymore
        for p in self.get_persons(**args):
#            logging.info('%s'% p)
            if not p.get_biographies():
                self.delete_person(p)
        return 

    def download_illustrations(self, source, overwrite=False, limit=None):
        """Download the illustrations associated with the biographies in the source.
        
        arguments:
             - source:  a Source instance

        returns:
             (total, skipped)
        """
        if not self.images_cache_local:
            raise Exception('Cannot download illustrations, self.images_cache_local has not been set')
        bios = self.get_biographies(source=source)
        i = 0
        total = len(bios)
        skipped = 0
        for bio in bios:
            i += 1
            if limit and i > limit:
                break
            for ill in bio.get_illustrations():
                try:
                    ill.download(overwrite=overwrite)
                except CantDownloadImage, err:
                    skipped += 1
                    logging.warning("can't download image: %s" % str(err))
        return total, skipped
                
    def add_biography(self, bio):
        """add the biography - or update it if an biography with the same id already is present in the system
        """
        # XXX - commented after we fallback on determining the id from 
        # filename if it is not defined inside the file
        #assert bio.get_value('local_id'), 'To add a biography to the repository, an id must be provided. This biography %s does not have that.\nE.g. <person><idno type="id">1234</idno></person>' % bio
        bio.repository = self
        if self.ENABLE_SVN:
            raise NotImplementedError()
        if self.ENABLE_DB:
            self.db.add_biography(bio)

    def get_most_similar_persons(self, **args):
        """get the most similar pairs of person, name we can find
           
           similar_to : a  bioport id
        returns:
            a list of triples (score, person1, person2)
        """
        return self.db.get_most_similar_persons(**args)
    
    def identify(self, person1, person2):
        """Identify the persons in this list (because they are really the same person)
        
        arguments:
            persons - a list of Person instances
        returns:
            a new Person instance representing the identified person
        """
        #the oldest identifier will be the canonical one
        return self.db.identify(person1, person2)


    def antiidentify(self, person1, person2):
        self.db.antiidentify(person1,person2)
    
    
    def unidentify(self, person):       
        return self.db.unidentify(person)
    def get_antiidentified(self):
        """return a list of anti-identified perons"""
        return self.db.get_antiidentified()
    
    def defer_identification(self, person1, person2):
        self.db.defer_identification(person1,person2)
        
    def get_deferred(self):
        return self.db.get_deferred()
    
    def get_identified(self, **args):
        return self.db.get_identified(**args)
            
    def redirect_identifier(self, bioport_id, redirect_to):
        """make sure that:
        1. all biographies associated with bioport_id will be associated with redirect_to
        2. the repository redirecs all references to bioport_id to redirect_to
       
        arguments:
            bioport_id - a bioport id
            redirect_to - a bioport id
        returns:
            None
        """
        if self.ENABLE_DB:
            self.db.redirect_identifier(bioport_id, redirect_to)
        if self.ENABLE_SVN:
            raise NotImplementedError#        id = self.get_identifier(bioport_id)
#        id.set_redirect_to(redirect_to)
#        id.set_biographies([])
#        self.save_identifier()


    def get_bioport_biography(self, person):
        """get, or if it does not yet exist, create, a biodes document that represents the interventions 
        of the editors in the biographical portal
        
        arguments:
            person - an instance of Person
        returns:
            an instance of Biography
        """    
        source = BioPortSource(id='placeholder')
                
        if not source.id in [s.id for s in self.get_sources()]:
            src = Source('bioport', repository=self)
            self.add_source(src)
            src.set_quality(10000)

        ls = self.get_biographies(source=source, person=person)
        if not ls:
            #create a new biography
            bio = Biography(id='%s/%s'  % (source.id, person.get_bioport_id()), source_id=source.id)
            bio._set_up_basic_structure()
            bio.set_value(local_id=person.get_bioport_id())
            bio.set_value(bioport_id=person.get_bioport_id())
            self.add_biography(bio)
            
            
            return bio
        else:
            if len(ls) != 1: 
                logging.warning( 'There was more than one Bioport Biography found for the person with bioport_id %s' %
                          person.get_bioport_id())
            ls = [(b.id, b) for b in ls]
            ls.sort(reverse=True) #we sort reverse, because that is also how we sort in "get_biographies"
            ls = [b for (x, b) in ls]
            return ls[0]
        
    def get_identifier(self, bioport_id):
        if self.ENABLE_DB:
            self.db.get_identifier()
        if self.ENABLE_SVN:
            raise NotImplementedError

    def invalidate_cache(self, attr):
        """
        arguments:
            attr - a string
        """
        
        assert attr in ['_sources']
        if hasattr(self, attr):
            delattr(self, attr)

    def get_occupations(self):
        return self.db.get_occupations()
    def get_occupation(self, id):
        return self.db.get_occupation(id)
    
    def get_category(self, id):
        return self.db.get_category(id)
    def get_categories(self):
        return self.db.get_categories()
    def get_places(self, *args, **kwargs):
        return self.db.get_places(*args, **kwargs)
    def  get_log_messages(self, **args):
        return self.db.get_log_messages(**args)
        


class PersonList(object):
    "This object provides a (possibly long) list of lazy-loaded Person objects"
    _records = []
    def __init__(self, query, repository):
        self.query = query
        self.repository = repository
        self._persons = {}
        
        if not isinstance(query, list):
            # We bypass SQLAlchemy ORM because it' expensive
            # and we don't need it for all results of the query
            # expecially when they are 24.000, like a serch for van der Aa
            try:
                self._records = query.session.execute(query._compile_context().statement,
                                  query._params).fetchall() 
            except InvalidRequestError:
                query.session.rollback() 
                self._records = query.session.execute(query._compile_context().statement,
                                  query._params).fetchall()
 
            self.column_names = [a.column.name for a in self.query._entities]
        else:
            self._records = query 
            
    @instance.memoize
    def __len__(self):
        if type(self.query) is list:
            return len(self.query)
        return self.query.count()
    
    def get_record(self, i):
        if self._records:
            # If we already have the record we mimic SqlAlchemy result object 
            # (accessible by column name as an attribute)
            return AttributeDict(dict(zip(self.column_names, self._records[i])))
        else:
            raise
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            new_list = PersonList(self._records[key], self.repository)
            new_list.column_names = self.column_names
            
            return new_list
        i = int(key)
        if i<0:
            i = len(self) + i
        if i in self._persons:
            return self._persons[i]
        r = self.get_record(i)
        person = Person(bioport_id=r.bioport_id,
                      repository=self.repository, record=r)
        self._persons[i] = person
        return person
    
class AttributeDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self
