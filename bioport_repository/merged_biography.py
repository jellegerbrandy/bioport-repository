#!/usr/bin/env python

from plone.memoize import instance
from biodes import BioDesDoc
from bioport_repository.data_extraction import BioDataExtractor
from lxml.etree import SubElement


class MergedBiography:    
    """ """
    
    def __init__(self, biographies):
        ls = [(b.get_source().quality,b.id, b) for b in biographies]
        ls.sort(reverse=True)
        ls = [b for q,i, b in ls]
        self._biographies = ls
    
    def to_string(self):
        """return a BioDes file that represents all information that we want to share"""
        return self.to_xml().to_string()
    
    @instance.memoize
    def to_xml(self): 
        doc = BioDesDoc()
        bioport_id = self.get_biographies()[0].get_bioport_id()
        #add the basic onfirmation
        doc.from_args(
            naam_publisher='Het Biografisch Portaal',
            url_biografie='http://www.biografischportaal.nl/persoon/%s' % bioport_id,
            url_publisher='http://www.biografischportaal.nl',
            namen=self.get_names(),
            bioport_id=bioport_id,
            sex = self.get_value('sex'),
        )
        #add the events
        for event_type in ['birth', 'death', 'funeral', 'baptism', 'floruit']:
            event = self.get_event(event_type)
            if event is not None:
                doc._add_event_element(event)
        #add illustrations
        for ill in self.get_illustrations():
            doc._add_figure(url=ill.source_url(), head=ill.caption)
        #add links to all sources
        for bio in self.get_biographies():
            if bio.get_source().id != 'bioport':
                #construct a bibl element
                bibl = SubElement(doc.get_element_biography(), 'bibl')
                publisher = SubElement(bibl, 'publisher')
                publisher.text = bio.get_value('name_publisher')
                ref = SubElement(bibl, 'ref')
                ref.attrib['target'] = bio.get_value('url_biography' )
                author = bio.get_value('author')
                if author:
                    for s in author:
                        el_author = SubElement(bibl, 'author') 
                        el_author.text = s
        return doc
        
    def get_biographies(self):
        return self._biographies
    
    def geboortedatum(self):
        event = self.get_event('birth')
        if event is not None:
            if event.get('when'):
                return event.get('when')
            elif event.find('date') is not None:
                return event.find('date').text
    def sterfdatum(self):
        event = self.get_event('death')
        if event is not None:
            if event.get('when'):
                return event.get('when')
            elif event.find('date') is not None:
                return event.find('date').text
    def get_event(self, type):
        for bio in self.get_biographies():
            if bio.get_event(type) is not None:
                return bio.get_event(type)
    def get_states(self, type):
        for bio in self.get_biographies():
            if bio.get_states(type):
                return bio.get_states(type)
        return []
    def get_value(self, k, default=None):
        """get the 'merged' value of for k
        
        for some fields, the 'merged value' is 'cumulative'
            (e.g. for illustraties we want to show all illustrations)
        for others it is the value from the 'most reliable' source 
            (e.g. for the place of birth)
        while for others (dates) we have special cases
        """
        cumulative_keys = [
               'illustraties',
               'beroep',
               ]
        
#        if k in ['geboortedatum',
#                 'sterfdatum',
#                 ]:
#            #get the longest 'consistent' value
#            #i.e. if we have
#            #    bio1:  2000
#            #    bio2:  2000-02
#            #reutrn 2000-02
#            #but  if we have
#            #    bio1 : 2000
#            #    bio2 : 2001-02
#            #then we return 2000
#            
#            result = ''
#            for bio in self.get_biographies():
#                val = bio.get_value(k)
#                if val and val.startswith(result):
#                    result = val
#            if result: #dont return result if no value was found, to retain behavior consistent with biography.get_value 
#                return result        
#        elif k in cumulative_keys:
        if k in cumulative_keys:
            result = []
            for bio in self.get_biographies():
                result += bio.get_value(k, [])
            if not result:
                result = default 
            return result
        
        else:
            for b in self.get_biographies():
                v = b.get_value(k)
                if v:
                    return v
                
        return default
    
    def title(self):
        for b in self.get_biographies():
            if b.title():
                return b.title()
            
    @instance.memoize   
    def get_names(self): 
        result = []
        for bio in self.get_biographies():
            if bio.source_id == 'bioport' and bio.get_names():
                return bio.get_names()
            else:
                for naam in bio.get_names():
                    if naam.volledige_naam() not in [n.volledige_naam() for n in result]:
                        result.append(naam)
        return result 

    def get_illustrations(self, default=[]):
        ls = []
        for bio in self.get_biographies():
            ls += bio.get_illustrations() 
        return ls or default
    
    def naam(self):
        """return the first name that you can find in the associated biographies"""
        for b in self.get_biographies():
            s= b.naam()
            if s:
                return s
            
