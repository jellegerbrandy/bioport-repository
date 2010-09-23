#!/usr/bin/env python

from plone.memoize import instance
from bioport_repository.local_settings import *
from bioport_repository.repocommon import is_valid_bioport_id
from bioport_repository.merged_biography import MergedBiography


class Person(object): 
    """A Person is an object that is identified with a bioport identifier
    
    it is usually associated with one or more Biography objects
    """
    
    def __init__(self, bioport_id, 
                       biographies=None, 
                       repository=None, 
                       record=None,  
                       status=None, 
                       remarks=None, 
                       score=None,
                ):
        """
        arguments:
            bioport_id - a unique identifier for this person
                bioport_id is MANDATORY because persons are by definitiion identified 
            biographies - a list of Biography instances
            repository - a Repository instance
            record - an instance of PersonRecord
            status - an integer
            remarks - a string
        """
        assert is_valid_bioport_id(bioport_id)
        self.id = self.bioport_id = bioport_id
        self.repository = repository
        self.record = record
        self.status = status
        self.remarks = remarks
        if record is not None:
            self.status = record.status
            self.remarks = record.remarks 
            self.has_illustrations = record.has_illustrations
        self.score = score 
        
    def __eq__(self, other):
        if type(other) == type(self) and other.bioport_id == self.bioport_id:
            return True

    @instance.clearafter
    def refresh(self):
        """empty the cache"""
        pass
    
    def singleton_id(self, id, **args):
        return self.id
    
    def __str__(self):
        if self.get_names():
	        return '<Person %s with id %s>' % (self.get_names()[0], self.id)
        else:
	        return '<Person with id %s>' % (self.id)
    
    __repr__ = __str__

    @instance.clearafter
    def add_biography(self, biography):
        if biography not in self.get_biographies():
            self.repository.add_biography(biography)
        
    @instance.memoize
    def get_biographies(self, source_id=None):
        """return all biographies that are known to be of this person
        
        returns: a list of Biography objects"""
        ls = self.repository.get_biographies(person=self, order_by='quality', source_id=source_id)            
        if source_id:
            if ls:
                return ls[0]
            else:
                return None
        else:
            return ls
        
    def get_bioport_id(self):
        return self.id#    def get_standard_biography(self):
    
    def get_sources(self):
        return [bio.get_source() for bio in self.get_biographies()]
    
    def get_quality(self):
        return max([bio.get_quality() for bio in self.get_biographies()])
    
    @instance.memoize
    def get_value(self, k, default=None):
        return self.get_merged_biography().get_value(k, default)
      
    @instance.memoize
    def get_merged_biography(self):
        """Return a Biography that represents the 'cascaded information' contained in the biographies of this person"""
        return MergedBiography(self.get_biographies())
    
    def get_bioport_biography(self):
        #convenience mthod
        return  self.repository.get_bioport_biography(self) 
       
    
    def get_names(self):    
        return self.get_merged_biography().get_names()
    def title(self):
        return self.get_merged_biography().title()

    @instance.memoize
    def name(self):
        try:
            return self._name
        except AttributeError:
            self._name = self.get_merged_biography().naam()
            return self._name

    naam = name 
    
    def redirects_to(self):
        """does this bioport_id redirect somewhere else? if yes, return that id, if not, return self.bioport_id"""
        return self.repository.redirects_to(self.get_bioport_id())
    
    def invalidate_cache(self, k):
        if hasattr(self, k):
            delattr(self, k)
            
    def search_source(self):
        result =[] 
        for name in self.get_names():
            result.append(name.volledige_naam())
        for bio in self.get_biographies():
            
            result.append(bio.get_text_without_markup())
        result = [unicode(s) for s in result]
        return '\n'.join(result)
    
    def snippet(self, term=None):
        """ask a snippet to each biography, and return the first we can find"""
#        search_source = self.record.search_source
#        return getSnippet(text=search_source, phrase=term, size=20, amount=3, start='<b>', end='</br>', boundary='\n\n', remove_tags=True)
    
        try:
            return self._snippet
        except AttributeError:
            self._snippet = ''
            for bio in self.get_biographies():
                s = bio.snippet()
                if s:
                    self._snippet = s
                    return self._snippet
                
    def get_comments(self):
        return self.repository.db.get_comments(bioport_id=self.id)

    def add_comment(self, **kwargs):
        kwargs['bioport_id'] = self.id
        return self.repository.db.add_comment(bioport_id=self.id, values=kwargs)

    def geboortedatum(self):
        return self.record.geboortedatum

    def sterfdatum(self):
        return self.record.sterfdatum

    def names(self):
        return self.record.names

    def thumbnail(self):
        return self.record.thumbnail

    def db_snippet(self):
        return self.record.snippet

    def geslachtsnaam(self):
        return self.record.geslachtsnaam

    def db_name(self):
        return self.record.naam



