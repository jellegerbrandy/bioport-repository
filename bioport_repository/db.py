import random
import os
import types
import re

from lxml import etree
from plone.memoize import instance
from zLOG import WARNING, LOG, INFO

import sqlalchemy
from sqlalchemy.exceptions import IntegrityError, InvalidRequestError
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import NoResultFound

from names.similarity import soundexes_nl, soundex_nl
from names.common import encodable, to_ymd , TUSSENVOEGSELS

from db_definitions import *
from datetime import datetime
from BioPortRepository.similarity.similarity import Similarity
from person import Person
from biography import Biography 
from source import Source
from BioPortRepository.db_definitions import CacheSimilarityPersons,\
    BioPortIdRecord, RelBioPortIdBiographyRecord, BiographyRecord, SourceRecord, STATUS_NEW, STATUS_VALUES

LENGTH = 8 #the length of a bioport id
ECHO = False

class DBRepository:
    NaamRecord = NaamRecord
    SoundexRecord = SoundexRecord
    SimilarityCache = SimilarityCache
    def __init__(self, db_connection, ZOPE_SESSIONS=False, user=None):
        
        self.connection = db_connection 
        self.user = user
        self.metadata = Base.metadata
        metadata = self.metadata 
        self._session = None
        if ZOPE_SESSIONS: 
            #XXX I could not get this to work, yet
            
            #setup z3c.saconfig
            #here for explanations:
            #http://svn.zope.org/z3c.saconfig/trunk/src/z3c/saconfig/README.txt?rev=102770&sortby=rev&view=markup
            from z3c.saconfig import EngineFactory
            engine_factory = EngineFactory(self.connection) #, convert_unicode=True, encoding='utf8')
            from zope import component
            from z3c.saconfig.interfaces import IEngineFactory
            component.provideUtility(engine_factory, provides=IEngineFactory)
            engine = engine_factory( )
            
            #
            from z3c.saconfig import GloballyScopedSession
            #
            
            utility = GloballyScopedSession()
            
            from z3c.saconfig.interfaces import IScopedSession
            component.provideUtility(utility, provides=IScopedSession)
            
            #
            from z3c.saconfig import Session 
            self.Session = Session
        else:
            #get the data from the db
            from sqlalchemy.orm import sessionmaker
            self.engine = Base.metadata.bind = metadata.bind = create_engine(self.connection, 
                    convert_unicode=True, 
                    encoding='utf8', 
                    echo=ECHO,
                    pool_recycle=3600, #set pool_recycle to one hour to avoig sql server has gone away errors
                    strategy="threadlocal",
                    )
            self.Session = sessionmaker(bind=self.engine)
            
            self.db = self 
            
    def get_session(self):
        if not self._session:
            self._session = self.Session()
        return self._session

    def query(self):
        return self.get_session().query
    def close_session(self):
        if self._session:
            self._session.close()
            self._session = None
            
    def add_source(self, src):
        assert src.id
        r = SourceRecord(id=src.id, url=src.url, description=src.description, xml=src._to_xml())
        session = self.get_session()
        
        session.add(r)
        msg = 'Added source'
        self.log(msg, r)
        session.commit()
        
    def save_source(self, src):
        session = self.get_session()
        try:
            r = session.query(SourceRecord).filter_by(id=src.id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return self.add_source(src) 
        r.url = src.url
        r.description = src.description
        r.quality = src.quality
        r.xml = src._to_xml()
        msg = 'saved source'
        self.log(msg, r)
        session.commit()
        
    def add_bioport_id(self, bioport_id):
        """Add a bioport id to the registry"""
        session = self.get_session()
        r_bioportid = BioPortIdRecord(bioport_id=bioport_id)
        session.add(r_bioportid)
        msg = 'Added bioport_id %s to the registry'
        self.log(msg, r_bioportid)
        try:
            session.commit()
        except:
            session.rollback()
            raise

    def get_source(self, source_id):
        """Get a Source instance with id= source_id """
        session = self.get_session()
        qry = session.query(SourceRecord) 
        qry = qry.filter(SourceRecord.id==source_id)
        r = qry.one()
        source = Source(id=r.id, url=r.url, description = r.description, quality=r.quality, xml=r.xml)
        return source
    
    def get_sources(self, order_by='quality', desc=True): 
        session = self.get_session()
        qry = session.query(SourceRecord)
        if order_by:
            if desc:
                qry = qry.order_by(sqlalchemy.desc(order_by))
            else:
                qry = qry.order_by(order_by)
        ls = qry.all()
        #session.close()
        return [Source(r.id, r.url, r.description, quality=r.quality, xml = r.xml, repository=self) for r in ls]

    def delete_source(self, source):
        session = self.get_session()
        qry =  session.query(SourceRecord).filter_by(id=source.id)
        try:
            r_source = qry.one()
        except sqlalchemy.orm.exc.NoResultFound:
            return
        
        self.delete_biographies(source=source)
        msg = 'Delete source %s' % source
        self.log(msg, r_source)
        session.delete(r_source)
        session.commit()
        #session.close()
        
    def get_bioport_ids(self):
        session = self.get_session()
        rs = session.query(BioPortIdRecord.bioport_id).distinct().all()
        return map(lambda x: x[0], rs)
   
    def delete_biographies(self, source=None, biography=None): 
        session = self.get_session()
        #delete also all biographies associated with this source
        if source:
            session.query(BiographyRecord).filter_by(source_id = source.id).delete()
        if biography:
            session.query(BiographyRecord).filter(BiographyRecord.id == biography.id).delete()
        session.commit()
        session.execute('delete rel from relbiographyauthor rel left outer join biography b on rel.biography_id = b.id where b.id is null')
        session.execute('delete a   from author a               left outer join relbiographyauthor rel on rel.author_id = a.id where rel.author_id is null')
        #delete all persons that have bioport_ids with no correspondeint biographies
        #session.execute('delete p   from person  p left outer join relbioportidbiography rel on p.bioport_id = rel.bioport_id left outer join biography b on rel.biography_id = b.id where b.id is null')
#        session.execute('delete n   from naam n               left outer join biography b on b.id = n.biography_id where b.id is null')
        session.execute('delete s   from soundex s            left outer join naam n  on s.naam_id = n.id where n.id is null')
        #delete orphans inthe similarity cache
        session.execute('delete c FROM cache_similarity c left outer join naam n1 on c.naam1_id = n1.id left outer join naam n2 on c.naam2_id = n2.id where n1.id is null or n2.id is null')
        
        session.commit()

    def delete_biography(self,biography):
        self.delete_biographies(biography=biography)
        
    def add_naam(self, naam, bioport_id, src):
        """ voeg eeen record toe aan de tabel "naam"
        
        arguments:
            naam - an instance of Naam 
            biography - an instance of biography
        """
        
        session = self.get_session()
        session.commit()
        item = NaamRecord()
        session.add(item)
        
        item.bioport_id = bioport_id
        item.volledige_naam = naam.guess_normal_form(change_xml=True)
        item.xml = naam.to_string()
        item.sort_key = naam.sort_key()
        item.src = src
#        item.src = src and unicode(src) or unicode(self.id)
        
        assert type(item.xml) == type(u'')
        assert type(item.sort_key) == type(u'')

        item.soundex = []
#        item.variant_of = variant_of
        
        for s in naam.soundex_nl():
            soundex = SoundexRecord()
            soundex.soundex = s
            item.soundex.append(soundex)
        
        try:
            session.commit()
        except UnicodeEncodeError, error:
            session.rollback()
            s = ''
            if not encodable(item.snippet, error.encoding):
                s +='item.snippet'
                
            error.reason += '\nOffending text is: %s' % s
            
            raise error
        id = item.id 
        return id
   
    def delete_names(self, bioport_id):
        session  = self.get_session()
#        session.execute('delete c FROM cache_similarity c join naam n1 on c.naam1_id = n1.id where n1.biography_id="%s"' % biography_id)
#        session.execute('delete c FROM cache_similarity c join naam n2 on c.naam1_id = n2.id where n2.biography_id="%s"' % biography_id)
        session.execute('delete s   from soundex s  left outer join naam n  on s.naam_id = n.id where n.bioport_id = "%s"' % bioport_id)
        session.execute('delete n   from naam n where bioport_id = "%s"' % bioport_id)

    def add_biography(self, biography):
        """add the biography to the database
        """
        return self.save_biography( biography)
    
    def save_biography(self, biography):
        session = self.get_session()
        try:
            r_biography = session.query(BiographyRecord).filter(BiographyRecord.id==biography.id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            #print 'biography %s was not found in the db, creating new record' % biography.id
            r_biography = BiographyRecord(id=biography.get_id())
            session.add(r_biography)
            
        r_biography.source_id = biography.source_id
       
        #register the biography in the bioportid registry
        self._register_biography(biography)
        
        #generated the biodes document only at the end (When all changes are made)  ?? which changes??
        r_biography.biodes_document = biography.to_string()
        r_biography.source_url = unicode(biography.source_url)
        
        session.commit()
        
        #update the information of the associated person (or add a person if the biography is new)
        default_status = self.get_source(biography.source_id).default_status
        self.update_person(biography.get_bioport_id(), default_status=default_status)
        
        msg  = 'saved biography with id %s' % (biography.id)
        self.log(msg=msg, record = r_biography)
        session.commit()

    def _add_author(self, author, biography_record):   
        """
        author - a string
        biography - a biography instance
        """
        
        
    def save_person(self, person):
        """save the information of this person in the database table
        
        person:
            a Person instance
        """
        session = self.get_session()
        try:
            r = session.query(PersonRecord).filter(PersonRecord.bioport_id==person.get_bioport_id()).one()
        except NoResultFound:
            r = PersonRecord(bioport_id=person.get_bioport_id())
            session.add(r)
        person.record = r
        if getattr(person, 'remarks', None) is not None:
            r.remarks = person.remarks
        if getattr(person, 'status', None):
            r.status = person.status

        msg = 'Changed person'
        self.log(msg, r)
        session.commit()       
        
    @instance.clearbefore
    def update_person(self,bioport_id, default_status=STATUS_NEW):
        """add or update a person table with the information contained in its biographies
        
        - bioport_id:  the id that identifies the person
        - default_status: the status given to the Person if it is a newly added person
        """
        session = self.get_session()
        
        #check if a person with this bioportid alreay exists
        try:  
            r_person = session.query(PersonRecord).filter_by(bioport_id=bioport_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            #if not, we add a new one
            r_person = PersonRecord(bioport_id=bioport_id) 
            session.add(r_person)
            r_person.status = default_status

        person = Person(bioport_id=bioport_id, record=r_person, repository=self)
        
        #refresh the names (move this code to "save_person"
        merged_biography = person.get_merged_biography()
        assert merged_biography.get_biographies(), person.bioport_id
        naam = merged_biography.naam()
        if naam:
            r_person.naam = naam.guess_normal_form()
            r_person.sort_key = naam.sort_key()
        else:
            msg = 'merged_biography should at least have one name defined! %s' % person.bioport_id
            raise Exception(msg)
            LOG.error('This is strange and should not happen: bioport id %s has no name' % person.bioport_id)
            
        r_person.categories = [RelPersonCategory(category_id=id) for state in merged_biography.get_states(type='categories')]
        r_person.has_illustrations = merged_biography.get_illustrations() and True or False
        r_person.search_source = person.search_source()
        r_person.sex = merged_biography.get_value('geslacht')
        r_person.sterfdatum = merged_biography.get_value('sterfdatum')
        if r_person.sterfdatum:
            r_person.sterfjaar = to_ymd(r_person.sterfdatum)[0]
        r_person.geboortedatum = merged_biography.get_value('geboortedatum')
        if r_person.geboortedatum:
            r_person.geboortejaar = to_ymd(r_person.geboortedatum)[0]
        r_person.geboorteplaats = merged_biography.get_value('geboorteplaats')
        r_person.sterfplaats = merged_biography.get_value('sterfplaats')
        r_person.names = ' '.join([unicode(name) for name in merged_biography.get_names()])
        r_person.geslachtsnaam = naam.geslachtsnaam()
        r_person.snippet = person.snippet()
        illustrations =  merged_biography.get_illustrations()
        r_person.thumbnail = illustrations and illustrations[0].thumbnail_url() or ''
        #update categories
        session.query(RelPersonCategory).filter(RelPersonCategory.bioport_id==bioport_id).delete()
        for category in person.get_merged_biography().get_states(type='category'):
            category_id = category.get('idno')
            assert type(category_id) in [type(u''), type('')], category_id
            try:
                category_id = int(category_id)
            except:
                msg = '%s- %s: %s' % (category_id, etree.tostring(category), person.bioport_id)
                raise Exception(msg)
            r = RelPersonCategory(bioport_id=bioport_id, category_id=category_id)
            session.add(r)
        
        #refresh the names 
        self.delete_names(bioport_id=bioport_id)
        
        #'the' source -- we take the first non-bioport source as 'the' source
        #and we use it only for filterling later
        src = [s for s in merged_biography.get_biographies() if s.source_id != 'bioport']
        if src:
            src = src[0].source_id
        else:
            src = None
            
        for naam in merged_biography.get_names():
            self.add_naam(naam=naam, bioport_id=bioport_id, src=src)
        
        self.update_soundex(bioport_id=bioport_id, s=r_person.names)
        self.update_name(bioport_id, s = r_person.names) 
        self.update_source(bioport_id, source_ids = [b.source_id for b in person.get_biographies()])
        session.commit()
        
    def update_persons(self):
        """update the information of all the persons in the database"""
       
        #XXX perhaps this should be "bioport_ids" from the registry, rather than persons from the Person table
        persons = self.get_persons()
        i = 0
        for p in persons:
            i += 1
#            print i, 'of', len(persons), ': update person'
            try:
                self.update_person(p.get_bioport_id())
            except Exception, error:
                #if this person does not have any biographical information associated with it
                #we delete from the person list
                for bio in p.get_biographies():
                    if bio.source_id != 'bioport' and bio.biodes_document:
                        #there is some real info
                        raise error
                #we did not re-raise the error, so ewe delete this perosn 
                session = self.get_session()
                session.commit()
                self.delete_person(p.bioport_id)
                session.commit()
                
                
    def update_name(self, bioport_id, s):
        """update the table person_name"""
        session = self.get_session()
        
        names = re.split('[^\w]+', s)
        #delete existing references
        session.query(PersonName).filter(PersonName.bioport_id == bioport_id).delete()
        for name in names:
            r =  PersonName(bioport_id=bioport_id, name=name) 
            session.add(r)
        session.commit()
 
        
    def update_soundex(self, bioport_id, s):
        """update the table person_soundex"""
        session = self.get_session()
        soundexes = soundexes_nl(s, group=2, length=20, filter_initials=True, filter_stop_words=False) #create long phonetic soundexes
        #delete existing references
        session.query(PersonSoundex).filter(PersonSoundex.bioport_id == bioport_id).delete()
        for soundex in soundexes:
            r = PersonSoundex(bioport_id=bioport_id, soundex=soundex) 
            session.add(r)
        session.commit()
    
 
    def update_source(self, bioport_id, source_ids):   
        """update the table person_source"""
        session = self.get_session()
        #delete existing references
        session.query(PersonSource).filter(PersonSource.bioport_id == bioport_id).delete()
        for source_id in source_ids:
            r = PersonSource(bioport_id=bioport_id, source_id=source_id) 
            session.add(r)
        session.commit()

    def tmp_update_soundexes(self):
        """update the person_soundex table in the database 
        
        use "update_persons" to update the information in the db (including person_soundex)
        """
        session = self.get_session()
        i = 0
        LOG('BioPort', INFO, 'updating all soundexes (this can take a while)')
        session.query(PersonSoundex).delete()
        persons = self.get_persons()
        for person in persons:
            i += 1
            if not i % 10:
                print '%s of %s' % (i, len(persons))
            names = person.record.names 
            self.update_soundex(person.bioport_id, names)
        
    def fresh_identifier(self):
        #make a random string of characters from ALPHANUMERIC of lenght LENGTH
        new_bioportid = ''.join([random.choice('0123456789') for i in range(LENGTH)])
        try:
            self.add_bioport_id(new_bioportid)
        except IntegrityError:
            #there is a small chacne that we already have used the bioport id before 
            #in that case we try agin
            return self.fresh_identifier()    
        return new_bioportid

    def _register_biography(self, biography): #, bioport_id=None):       
        """register the biography in the bioport registry and assign it a bioport_id if it does not have one
       
        arguments:
            biography: a Biography instance
            
        we 
            1. try to find a bioport id in the biography (in the XML document of the biography)
            2. try to find a bioport id in the registry associated with biography.get_idno()
            3. create a new bioport identifier
        """
        session = self.get_session()
        
        #try to find a bioport id in the Biography
        #XXX this needs to be optimized
        if biography.get_bioport_id() :
            #if it has a bioport_id define,d it should already have been registered
            bioport_id = biography.get_bioport_id()
            try:
                assert session.query(BioPortIdRecord).filter(BioPortIdRecord.bioport_id==bioport_id).one()
            except:
                msg = 'This biography seems to have a bioport_id defined that is not present in the database'
                raise Exception(msg)
        else:
            #try to find a bioport id in the reistry for this biography
            qry = session.query(RelBioPortIdBiographyRecord).filter_by(biography_id=biography.id)
            rs = qry.all()
            if len(rs) == 1:
                #this biography is already registered w
                r_relbioportidbiography = rs[0] 
                bioport_id = r_relbioportidbiography.bioport_id
            else:
                bioport_id = self.fresh_identifier()
        
        #now we update the biography as well as the registry
        if bioport_id != biography.get_bioport_id():
            biography.set_value('bioport_id', bioport_id)
        
        #update the registry  
        #if it is not connected to the new biography, we add the relation
        qry = session.query(RelBioPortIdBiographyRecord)
        qry = qry.filter_by(biography_id=biography.id)
        qry = qry.filter_by(bioport_id=bioport_id) 
        try: 
            qry.one()
        except NoResultFound:
            #delete any old information we may have in the registry about this biography
            session.query(RelBioPortIdBiographyRecord).filter(RelBioPortIdBiographyRecord.biography_id==biography.id).delete()
                
            #now add the new relation
            session.add(RelBioPortIdBiographyRecord(bioport_id=bioport_id, biography_id=biography.id) )
            session.commit()
            

        return bioport_id
    
    def count_biographies(self, source=None):
        """return the number of biographies in the database, 
        excluding those of the source 'bioport'"""
        qry = self.get_session().query(BiographyRecord)
        if source:
            qry = qry.filter(BiographyRecord.source_id==source.id)
        else:
        
            qry = qry.filter(BiographyRecord.source_id!='bioport')
        return qry.count()
    
    def get_biographies(self, 
        source=None,
        source_id=None,
        person=None,
#        biography_id=None,
        local_id=None,
        order_by=None,
        limit=None,
#        exclude=None,
        ): 
        """
       
        arguments:
            source  - an instance of Source
            person - an instance of Person
            order_by - a string - the name of a column to sort by
            local_id - the 'local id' of the biography - somethign fo the form 'vdaa/w0269' 
            #biography_id - the id of the biography - constructed from the source and the local_id
#            exclude - a source id or list of source ids - biographies from these sources are not return
#                e.g. get_biographies(exclude='bioport')
        """
        #XXX implement order_by
            
        session = self.get_session()
        qry = session.query(BiographyRecord)
        if source:
            if type(source) in types.StringTypes:
                source_id = source
            else:
                source_id = source.id
                
        if source_id:
            qry = qry.filter_by(source_id=source_id)
            
        if local_id:
            qry = qry.filter_by(id=local_id)
            
        if person:
            qry = qry.join((RelBioPortIdBiographyRecord, BiographyRecord.id==RelBioPortIdBiographyRecord.biography_id))
            qry = qry.filter(RelBioPortIdBiographyRecord.bioport_id==person.get_bioport_id())
        
        if order_by == 'quality':
            qry = qry.join((SourceRecord,SourceRecord.id==BiographyRecord.source_id))
            qry = qry.order_by(sqlalchemy.desc(order_by))
            qry = qry.order_by(BiographyRecord.id)
        elif order_by:
            qry = qry.order_by(order_by)
        if limit:
            qry = qry.limit(limit)
            
        ls = qry.all()
#        if exclude:
#            if type(exclude)  in types.StringTypes:
#               exclude = [exclude]  
#            ls = [b for b in ls if r.source_id not in exclude]
        ls = [Biography(id=r.id, source_id=r.source_id, repository=self.repository, biodes_document =r.biodes_document, source_url=r.source_url, record=r) for r in ls]
        #session.close()
        return ls

    def get_biography(self, **args):
        ls = self.get_biographies(**args)
        assert len(ls) == 1, 'Expected to find exactly one biography with the following arguments (but found %s): %s' % (len(ls), args)
        return ls[0]

    def count_persons(self):
        
        session=self.get_session()
        qry = session.query(PersonRecord)
        return qry.count()
    
    def get_persons(self, 
            **args
            ):
        qry = self._get_persons_query(**args)
        #executing the qry.statement is MUCH faster than qry.all()
        ls = self.get_session().execute(qry.statement)
        #but - do we want to make Person objects for each of these things 
        #(yes, because we use lots of information later - for example for navigation)
        #XXX (but is is very expensive)
        result = [Person(bioport_id=r.bioport_id, repository=self.repository, record=r) for r in ls]
        return result   
    

    def _get_date_filter(self, data, datetype):
        """
        This function builds a sqlalchemy filter using data in 'data'.
        datetype is used to extract variables from data.
        datetype can be either "geboorte" or "sterf"
        """
        datdag_min = data[datetype + 'dag_min']
        datmaand_min = data[datetype + 'maand_min']
        datjaar_min = data[datetype + 'jaar_min']
        datdag_max = data[datetype + 'dag_max']
        datmaand_max = data[datetype + 'maand_max']
        datjaar_max = data[datetype + 'jaar_max']
        maand_min = int(datmaand_min or 1)
        dag_min = int(datdag_min or 1)
        maand_max = int(datmaand_max or 12)
        dag_max = int(datdag_max or 31)
        date_filter = "TRUE"
        field = getattr(PersonRecord, datetype + 'datum', None)
        if datetype == 'levend' and not (datjaar_min or datjaar_max):
            # Everybody was alive in every period of the year, so this
            # does not make any sense
            return date_filter
        if datjaar_min or datjaar_max:
            jaar_min = int(datjaar_min or 0)
            jaar_max = int(datjaar_max or 9999)
            start_date = "%04i-%02i-%02i" % (jaar_min, maand_min, dag_min)
            end_date = "%04i-%02i-%02i" % (jaar_max, maand_max, dag_max)
            if datetype == 'levend':
                date_filter = and_(PersonRecord.geboortedatum<start_date,
                              PersonRecord.sterfdatum>end_date)
            else:
                date_filter = and_(field >= start_date,
                                   field <= end_date)
        elif (datmaand_min or datdag_min
              or datmaand_max or datdag_max):
            SUBSTRING = sqlalchemy.func.SUBSTRING
            no_year = SUBSTRING(field, 6, 5)
            start_date = "%02i-%02i" % (maand_min, dag_min)
            end_date = "%02i-%02i" % (maand_max, dag_max)
            myoperator = and_
            if start_date>end_date:
                myoperator = or_
            date_filter = myoperator(no_year >= start_date, no_year <= end_date)
            # We want the month to be specified, i.e. at least a 7-char date
            date_filter = and_(date_filter, sqlalchemy.func.length(field)>=7)
        return date_filter

    def _get_persons_query(self,             
        bioport_id=None,
#        beroep_id=None,
#        auteur_id=None,
        beginletter=None,
        category=None,
        geboortejaar_min=None,
        geboortejaar_max=None,
        geboortemaand_min=None,
        geboortemaand_max=None,
        geboortedag_min=None,
        geboortedag_max=None,
        levendjaar_min=None,
        levendjaar_max=None,
        levendmaand_min=None,
        levendmaand_max=None,
        levenddag_min=None,
        levenddag_max=None,
        geboorteplaats = None,
        geslacht=None,
        has_illustrations=None, #boolean: does this person have illustrations?
        is_identified=None,
        match_term=None, #use for myqsl 'matching' (With stopwords and stuff)
        order_by='sort_key', 
        place=None,
        search_term=None,  #
        search_name=None, #use for mysql REGEXP matching
        search_soundex=None, #a string - will convert it to soundex, and try to match (all) of these
        any_soundex=[], #a list of soundex expressions - try to match any of these
        source_id=None,
        sterfjaar_min=None,
        sterfjaar_max=None,
        sterfmaand_min=None,
        sterfmaand_max=None,
        sterfdag_min=None,
        sterfdag_max=None,
        sterfplaats = None,
        start=None,
        size=None,
        status=None,
        hide_invisible=True, #if true, do not return "invisible" persons, such as those marked as "troep"
        hide_foreigners=False, #if true, do not return persons marked as "buitenlands"
        where_clause=None,
        ):
        """
        returns:
            a Query instance
        """
        session=self.get_session()
        qry = session.query(
            PersonRecord.bioport_id,
            PersonRecord.status,
            PersonRecord.remarks,
            PersonRecord.has_illustrations,
            PersonRecord.geboortedatum,
            PersonRecord.sterfdatum,
            PersonRecord.naam,
            PersonRecord.names,
            PersonRecord.geslachtsnaam,
            PersonRecord.thumbnail,
            PersonRecord.snippet,
            PersonRecord.timestamp,
            )
        
        if is_identified:
            #a person is identified if another bioport id redirects to it
            #XXX: this is not a good definition
            PBioPortIdRecord = aliased(BioPortIdRecord)
            qry = qry.join((PBioPortIdRecord, PersonRecord.bioport_id == PBioPortIdRecord.redirect_to))
#            qry = qry.join(BioPortIdRecord).join(RelBioPortIdBiographyRecord)
#            qry = qry.filter(RelBioPortIdBiographyRecord.biography_id.count() > 1)
            
        if hide_invisible:
            qry = qry.filter(not_(sqlalchemy.func.ifnull(PersonRecord.status.in_([5, 9]), False)))
        if hide_foreigners:
            qry = qry.filter(not_(sqlalchemy.func.ifnull(PersonRecord.status.in_([11]), False)))
            
#            (1, 'nieuw'),
#            (2, 'bewerkt'),
#            (3, 'moeilijk geval'),
#            (5, 'moeilijk geval (troep)'),
#            (4, 'klaar'), 
#            (7, 'te weinig informatie'), 
#            (8, 'familielemma'), 
#            (9, 'verwijslemma'), 
#            (10, 'nader onderzoek nodig'), 
#            (11, 'buitenlands'), 
#            (12, 'nog niet bewerkt'),
#
        if beginletter:
            qry = qry.filter(PersonRecord.naam.startswith(beginletter))
            
        if bioport_id: 
            qry = qry.filter(PersonRecord.bioport_id==bioport_id)
            
        if category:
            if category in ['0']:
                category = None
            qry = qry.join(RelPersonCategory)
            qry = qry.filter(RelPersonCategory.category_id==category)


        geboorte_date_filter = self._get_date_filter(locals(), 'geboorte')
        qry = qry.filter(geboorte_date_filter)
        sterf_date_filter = self._get_date_filter(locals(), 'sterf')
        qry = qry.filter(sterf_date_filter)
        levend_date_filter = self._get_date_filter(locals(), 'levend')
        qry = qry.filter(levend_date_filter)
        if geboorteplaats:
            if '*' in geboorteplaats:
                dafilter = PersonRecord.geboorteplaats.like(
                        geboorteplaats.replace('*', '%')
                    )
                qry = qry.filter(dafilter)
            else:
                qry = qry.filter(PersonRecord.geboorteplaats == geboorteplaats)
        if sterfplaats:
            if '*' in sterfplaats:
                dafilter = PersonRecord.sterfplaats.like(
                        sterfplaats.replace('*', '%')
                    )
                qry = qry.filter(dafilter)
            else:
                qry = qry.filter(PersonRecord.sterfplaats == sterfplaats)

        if geslacht:
            qry= qry.filter(PersonRecord.sex==geslacht)
            
        if has_illustrations is not None:
            qry = qry.filter(PersonRecord.has_illustrations==has_illustrations) 
        
        if match_term:
            qry = qry.filter(PersonRecord.naam.match(match_term))
            
#        if search_term:
#            search_term = search_term.replace('*', '.*')
#            search_term = search_term.replace('?', '.')
#            for s in search_term.split():
#                qry = qry.filter(PersonRecord.search_source.op('regexp')('[[:<:]]%s[[:>:]]' % s))
        if search_term:
            # Mysql uses the OR operator by default
            # with a '+' in front of each word we use the AND operator
            words = re.split('\W+', search_term)
            words_with_plus = ['+' + word for word in words]
            words_query = ' '.join(words_with_plus)
            qry = qry.filter('match (search_source) against '
                              '("%s" in boolean mode)' % words_query)
        qry = self._filter_search_name(qry, search_name)
        qry = self._filter_soundex(qry, search_soundex)
        if any_soundex:
            qry = qry.join(PersonSoundex)
            qry = qry.filter(PersonSoundex.soundex.in_( any_soundex))
                
        if source_id:
            qry = qry.join(PersonSource)
            if type(source_id) == types.ListType:
                source_id = filter(None, source_id)
                if source_id:
                    qry = qry.filter(PersonSource.source_id.in_(source_id))
            else:
                qry = qry.filter(PersonSource.source_id==source_id)
        
        if status:
            if status in ['0']:
                status = None
            qry = qry.filter(PersonRecord.status == status)

        if sterfjaar_min:
            qry = qry.filter(PersonRecord.sterfjaar >= sterfjaar_min)
        if sterfjaar_max:
            qry = qry.filter(PersonRecord.sterfjaar <= sterfjaar_max)
        if where_clause:
            qry = qry.filter(where_clause)

        if order_by:
            if order_by == 'random':
                #XXX this is perhaps a slow way of doing is; for our purposes it is also enough to pick a random 
                #id, and do somethin like "where id > randomlypickednumber limit XXX"
                some_bioportid = ''.join([random.choice('0123456789') for i in range(LENGTH)])
                qry = qry.filter(PersonRecord.bioport_id > some_bioportid)
            else:
                qry = qry.order_by(order_by)        
        if size:
            qry = qry.limit(size)
        qry = qry.distinct()
#        print qry.statement
        return qry
    
    def _filter_search_name(self, qry, search_name):
        #if the name argument is between quotation marts, we search "exact"
        #(but we still ignore the order)
        if not search_name:
            return qry
        if search_name.startswith('"'):
            search_name = search_name[1:]
            if search_name.endswith('"'):
                search_name = search_name[:-1]
                
            for s in search_name.split():
                #changed this to a faster separate table with the "words" that we are searching for 
#                    qry = qry.filter(PersonRecord.names.op('regexp')(u'[[:<:]]%s[[:>:]]' % s))
                alias = aliased(PersonName)
                qry = qry.join(alias)
                if '?' in s or '*' in s:
                    s = s.replace('?', '_')
                    s = s.replace('*', '%')
                    qry = qry.filter(alias.name.like(s))
                else: 
                    qry = qry.filter(alias.name ==s)
        else:
            qry = self._filter_soundex(qry, search_name)
        return qry
 
    def _filter_soundex(self, qry, search_soundex):
        if search_soundex:
            soundexes = soundexes_nl(
                 search_soundex, 
                 length=-1, 
                 group=2,
                 filter_initials=False, 
                 filter_stop_words=False, 
                 wildcards=True,
                 )
            if len(soundexes)==1 and  '?' in soundexes[0] or '*' in soundexes[0]:
                #we can use wildcards, but only if we have a single soundex
                s = soundexes[0]
                s = s.replace('?', '_')
                s = s.replace('*', '%')
                qry = qry.join(PersonSoundex)
                qry = qry.filter(PersonSoundex.soundex.like(s))
            else:
                for s in soundexes:
                    alias = aliased(PersonSoundex)
                    qry = qry.join(alias)
                    qry = qry.filter(alias.soundex == s)
        return qry

    def get_person(self, bioport_id):
        session = self.get_session()
        qry = session.query(PersonRecord).filter(PersonRecord.bioport_id ==bioport_id)
        try:
            r = qry.one()
        except NoResultFound:
            id = self.redirects_to(bioport_id)
            if id != bioport_id:
                return self.get_person(id)
            else:
                return None
        
        person = Person(bioport_id=bioport_id, record=r, repository=self)
        return person

    def delete_person(self, person):
        
        session = self.get_session()
        try:
            r = session.query(PersonRecord).filter(PersonRecord.bioport_id==person.get_bioport_id()).one()
            session.delete(r) 
            session.query(PersonSoundex).filter(PersonSoundex.bioport_id==person.bioport_id).delete()
            session.commit()
            msg = 'Deleted person %s' % person
            self.log(msg, r)
        except NoResultFound:
            session.rollback()
            
            



    def get_authors(self, 
            biography=None,
            beginletter=None,
            search_term=None,
            order_by='name',
            ):
        assert 0, 'get_authors is (perhaps temporarily) disabled (because we do not use it and it eats time and memory)'
        
        session = self.get_session()
        qry = session.query(AuthorRecord)
        if biography:
            qry = qry.filter(AuthorRecord.biographies.any(biography_id=biography.id))
  
        if beginletter:
            qry = qry.filter(AuthorRecord.name.like('%s%%' % beginletter))
        if search_term:
            qry = qry.filter(AuthorRecord.name.like('%%%s%%' % search_term))
        qry = qry.order_by(order_by)
        ls = qry.all()
        return ls
    
    def get_author(self, author_id):
        session = self.get_session()
        qry = session.query(AuthorRecord)
        qry = qry.filter(AuthorRecord.id == author_id)
        return qry.one()
    
    def redirect_identifier(self, bioport_id,redirect_to):
        """add a 'redirect' instruction to this bioport_id"""
        assert bioport_id
        session=self.get_session()
        qry = session.query(BioPortIdRecord).filter_by(bioport_id=bioport_id)
        
        r = qry.one()
        #add a new record for the redirection
        r.redirect_to = redirect_to
        session.commit()


    def redirects_to(self, bioport_id):
        """follow the rederiction chain to an endpoint
        
        returns:
            a bioport identifier
        """
        orig_id = bioport_id
        chain = [orig_id]
        i = 0
        while True:
            qry = self.get_session().query(BioPortIdRecord).filter(BioPortIdRecord.bioport_id==bioport_id)
            i += 1
            try:
                r_bioportid = qry.one() 
                if  r_bioportid.redirect_to:
                    if r_bioportid.redirect_to in chain:
                        break
                    else:
                        chain.append(r_bioportid.redirect_to )
                else:
                    break
                
            except:
                break
        return chain[-1]
    
    def fill_similarity_cache(self, 
        person=None, 
        k=20, 
        refresh=False, 
        limit=None,
        source_id=None,
        minimal_score=0.86,
        ):
        """fill a table CacheSimilarityPersons with, for each name in the index, a record with the 20 most similar other names in the index
       
           arguments:
               k - the maxium number of 'most similar items'  to add
               person - an instance of Person
               refresh - throw away existing data and calculate from 0 (should only be used if function has changed)
               limit - an integer - compute only for that amount of persons
        """     
        
        session = self.db.get_session()
        
        if refresh:
            #if refresh is true, we delete all relevant records
            LOG('BioPort', INFO, 'Refilling similarity table')
            LOG('BioPort', INFO, 'Deleting all records from cachesimilaritypersons')
            qry = session.query(CacheSimilarityPersons)
            if person:
                #just remove the records of this person
                qry = qry.filter(CacheSimilarityPersons.bioport_id1==person.get_bioport_id())  
                qry.delete()   
                qry = qry.filter(CacheSimilarityPersons.bioport_id2==person.get_bioport_id())  
                qry.delete()   
            else:
                #print 'deleting all information from cache_similarity_persons'
                if source_id:
                    qry = qry.outerjoin((
                        RelBioPortIdBiographyRecord, 
                        or_( RelBioPortIdBiographyRecord.bioport_id==CacheSimilarityPersons.bioport_id1,
                             RelBioPortIdBiographyRecord.bioport_id==CacheSimilarityPersons.bioport_id2
                        )
                    ))
                    qry = qry.join((BiographyRecord, 
                           BiographyRecord.id ==RelBioPortIdBiographyRecord.biography_id,
                           ))
                    qry = qry.filter(BiographyRecord.source_id==source_id)
                    #mm, this fails fro some obscure reason
                    #qry.delete()
                    #hack our way to a delete query
                    s = unicode(qry.statement)
                    s = s[s.find('FROM'):]
                    s = s % ("'%s'" %  source_id)
                    s = 'DELETE cache_similarity_persons %s' % s
                    print s
                    session.execute(s)
                else:
                    qry.delete()
            session.commit() 
            
            
        #if the person argument is not given, we update for all persons
        if person:
            persons = [person]
        else:
            persons = self.get_persons(source_id=source_id)
            
        i = 0
        
        for person in persons:
            i += 1
            if limit and i > limit:
                break
            LOG('BioPort', INFO, 'computing similarities for %s out of %s: %s' % (i, len(persons), person))
            bioport_id = person.bioport_id
            #check if we have alread done this naam
            qry = session.query(CacheSimilarityPersons.bioport_id1)
            qry = qry.filter_by(bioport_id1=bioport_id, bioport_id2=bioport_id) 
            
            if qry.all():
                #we have already done this person , and we did not explicitly call for a refresh
#                print 'already done'
                continue
            else:
                #we add the identity score so that we can check later that we have 'done' this record, 
                self.add_to_similarity_cache(bioport_id, bioport_id, score=1.0)
            
            #now get a list of potential persons
            #we create a soundex on the basis of the last name of the person
            combined_name = ' '.join([n.guess_geslachtsnaam() or n.volledige_naam() for n in person.get_names()])
#            print combined_name
            soundexes = soundexes_nl(
                 combined_name, 
                 length=-1, 
                 group=2,
                 filter_initials=True, 
                 filter_stop_words=False, #XXX look out withthis: 'koning' and 'heer' are also last names 
                 filter_custom=TUSSENVOEGSELS,
                 wildcards=False,
                 )
            
            LOG('BioPort', INFO, 'searching for persons matching any of %s' % soundexes)
            if not soundexes:
                persons_to_compare = []
            else:
                persons_to_compare = self.get_persons(any_soundex = soundexes)
            LOG('BioPort', INFO, 'comparing to %s other persons' % len(persons_to_compare))
            #compute the similarity
            similarity_computer = Similarity(person, persons_to_compare)
            similarity_computer.compute()
            similarity_computer.sort()
            similar_persons =  similarity_computer._persons
            if len(similar_persons) > 1:
                most_sim = similar_persons[1]
                LOG('BioPort', INFO, 'highest similarity score: %s (%s)' % (most_sim.score, most_sim))
            else:
                LOG('BioPort', INFO, 'no similar persons found')
            for p in similarity_computer._persons[:k]:
                if p.score > minimal_score:
                    self.add_to_similarity_cache(person.bioport_id, p.bioport_id, p.score)
                    try:
                        msg =  '%s|%s|%s|%s|%s|' % (person.bioport_id, p.bioport_id, p.score, person.naam(), p.naam())
                        LOG('BioPort', INFO, msg)
                    except UnicodeEncodeError:
                        LOG('BioPort', INFO, 'scores could not be printed due to UnicodeEncodeError')
            #print '-' * 20
            session.commit()
            
        session.expunge_all() # removes objects from session
        session.close()  
    
    def add_to_similarity_cache(self,bioport_id1, bioport_id2,score):
        session = self.get_session()
        id1 = min(bioport_id1, bioport_id2)
        id2 = max(bioport_id1, bioport_id2)
        r = CacheSimilarityPersons(bioport_id1=id1, bioport_id2=id2, score=score)
                        
        session.add(r)
        try:
            session.commit()
        except IntegrityError: 
            #this is (probably) a 'duplicate entry', 
            #caused by having already added the relation when we processed item
            #we update the record to reflect the highest score
            session.rollback()
                                
            r_duplicate = session.query(CacheSimilarityPersons).filter_by(bioport_id1=id1, bioport_id2=id2).one()
            if score > r_duplicate.score:
                r_duplicate.score = score
                session.commit()
        
    def get_most_similar_persons(
         self, 
         start=0, 
         size=50, 
         refresh=False, 
#         similar_to=None,
         source_id=None,                       
         status=None,
         search_name=None,
         bioport_id=None,
         ):
        session = self.get_session() 
        if refresh: 
            #(re) fill the cache
            self.fill_similarity_cache(refresh=refresh)            
        qry = session.query(CacheSimilarityPersons)
        qry = qry.outerjoin((AntiIdentifyRecord,  
             and_( 
                  AntiIdentifyRecord.bioport_id1==CacheSimilarityPersons.bioport_id1, 
                  AntiIdentifyRecord.bioport_id2==CacheSimilarityPersons.bioport_id2, )
             ))
        qry = qry.outerjoin((DeferIdentificationRecord,  
             and_( 
                  DeferIdentificationRecord.bioport_id1==CacheSimilarityPersons.bioport_id1, 
                  DeferIdentificationRecord.bioport_id2==CacheSimilarityPersons.bioport_id2, )
             ))
        qry = qry.join((BioPortIdRecord, BioPortIdRecord.bioport_id==CacheSimilarityPersons.bioport_id1))
        BioPortIdRecord2 = aliased(BioPortIdRecord)
        qry = qry.join((BioPortIdRecord2, BioPortIdRecord2.bioport_id==CacheSimilarityPersons.bioport_id2))
          
        
        qry = qry.filter(CacheSimilarityPersons.bioport_id1 != CacheSimilarityPersons.bioport_id2)
        # not antiidentical */ 
        qry = qry.filter(AntiIdentifyRecord.bioport_id1 == None)
        qry = qry.filter(AntiIdentifyRecord.bioport_id2 == None)
        #    not deferred */ 
        qry = qry.filter(DeferIdentificationRecord.bioport_id1 == None)
        qry = qry.filter(DeferIdentificationRecord.bioport_id2 == None)
        
        qry = qry.filter(BioPortIdRecord.redirect_to == None)
        qry = qry.filter(BioPortIdRecord2.redirect_to == None)
        
        if bioport_id:
            qry = qry.filter(or_(CacheSimilarityPersons.bioport_id1 == bioport_id, CacheSimilarityPersons.bioport_id2==bioport_id))
        
        if not type(source_id) == type([]):
            source_id = [source_id]
        source_id = filter(None, source_id)
        if source_id:
            qry = qry.join((
                RelBioPortIdBiographyRecord, 
                 RelBioPortIdBiographyRecord.bioport_id==CacheSimilarityPersons.bioport_id1,
            ))
            qry = qry.join((BiographyRecord, 
                   BiographyRecord.id ==RelBioPortIdBiographyRecord.biography_id,
                   ))
            qry = qry.filter(BiographyRecord.source_id.in_(source_id))
#            qry = qry.filter(RelBioPortIdBiographyRecord.biography.source_id==source_id)
            RelBioPortIdBiographyRecord2 = aliased(RelBioPortIdBiographyRecord)
            qry = qry.join((
                RelBioPortIdBiographyRecord2, 
                 RelBioPortIdBiographyRecord2.bioport_id==CacheSimilarityPersons.bioport_id1,
            ))
            BiographyRecord2 = aliased(BiographyRecord)
            qry = qry.join((BiographyRecord2, 
                   BiographyRecord2.id ==RelBioPortIdBiographyRecord2.biography_id,
                   ))
            qry = qry.filter(BiographyRecord2.source_id.in_(source_id))
        if search_name:
            qry = qry.join((PersonRecord, 
               PersonRecord.bioport_id==CacheSimilarityPersons.bioport_id1
                ))
            PersonRecord2 = aliased(PersonRecord)
            qry = qry.join((PersonRecord2, 
                    PersonRecord2.bioport_id==CacheSimilarityPersons.bioport_id2
                 ))
            qry = self._filter_search_name(qry, search_name)         
        
        qry = qry.distinct()
        qry = qry.order_by(desc(CacheSimilarityPersons.score))
        qry = qry.order_by(CacheSimilarityPersons.bioport_id1)
        qry = qry.slice(start, start + size)
        LOG('BioPort',INFO, 'executing %s'% qry.statement)
        ls = [(r.score, Person(r.bioport_id1, repository=self, score=r.score), Person(r.bioport_id2, repository=self, score=r.score)) for r in session.execute(qry)]
        return ls
     
    def XXX_fill_most_similar_persons_cache(self, refresh=False): #, start=0, size=20):
        #this gives us the most similar SimilarityCacheopbjects
        session = self.db.get_session()
        qry = session.query(CacheSimilarityPersons)
        if not refresh and qry.count():
            return
        else:
            LOG.info('fill most similar persons cache' )
            qry.delete()
            session.commit()
        
        i = 0
        min_score = 0

       
        sql = """SELECT score, n1.id, n1.xml, n2.id, n2.xml,
        r1.bioport_id as bioport_id1, 
        r2.bioport_id as bioport_id2
        FROM cache_similarity c 
inner join naam n1
on n1.id = c.naam1_id
inner join naam n2
on n2.id = c.naam2_id
inner join biography b1
on n1.biography_id = b1.id
inner join biography b2
on n2.biography_id = b2.id
inner join relbioportidbiography r1
on r1.biography_id = b1.id
inner join relbioportidbiography r2
on r2.biography_id = b2.id
left outer join antiidentical a
on 
    a.bioport_id1 =  IF( r1.bioport_id < r2.bioport_id, r1.bioport_id, r2.bioport_id)
     and a.bioport_id2 = IF( r1.bioport_id < r2.bioport_id, r2.bioport_id, r1.bioport_id)
left outer join defer_identification d
on 
    d.bioport_id1 =  IF( r1.bioport_id < r2.bioport_id, r1.bioport_id, r2.bioport_id) 
    and d.bioport_id2 = IF( r1.bioport_id < r2.bioport_id, r2.bioport_id, r1.bioport_id)
left outer join bioportid b 
on ((b.bioport_id = r1.bioport_id and b.redirect_to = r2.bioport_id) or (b.bioport_id = r1.bioport_id and b.redirect_to = r2.bioport_id))
where 
n1.id != n2.id /*different names */
and r1.bioport_id != r2.bioport_id /*different persones */
and a.bioport_id1 is null /* not antiidentical */ 
and a.bioport_id2 is null
and d.bioport_id1 is null /*not deferred */ 
and d.bioport_id2 is null
and b.bioport_id is null /* not redirected to others */
and b.redirect_to is null
and b1.source_id != b2.source_id /*from different sources */
order by score desc
        """
                   
        rs = session.execute(sql)
        for r in rs:
            score = r.score 
            id1 = r.bioport_id1            
            id2 = r.bioport_id2            
            
#            if id1 != id2: # and not qry.count():
            #p1 = Person(id1, repository=self)
            #p2 = Person(id2, repository=self)
            #srcs1 = [src for src in [bio.get_source() for bio in p1.get_biographies()]]
            #srcs2 = [src for src in [bio.get_source() for bio in p2.get_biographies()]]
            #srcs_intersection = [s for s in srcs1 if s in srcs2]
            #if srcs_intersection == []:
            i += 1
            id1, id2 = (min(id1, id2), max(id1, id2)) 
            r_cache = CacheSimilarityPersons(score=score, bioport_id1=id1, bioport_id2=id2)
            session.add(r_cache) 
            try:
                session.commit()  
            except:
                #this must be a duplicate - which is no problem 
                #XXX but we must take the highest score
                session.rollback()
                r_existing = session.query(CacheSimilarityPersons).filter(CacheSimilarityPersons.bioport_id1==id1).filter(CacheSimilarityPersons.bioport_id2==id2).one()
                if score > r_existing.score:
                    r_existing.score = score
                    session.commit()
                
            #give some minimal user feedback
            if i % 100 == 0:
                LOG.info(str(i))
                    
                    #if i > start+size:
                    #    return
        session.commit()
        
        #notify caching machinery that the table is filled
        self._cache_filled_similarity_persons = True 
        LOG.info('done')
        
    def identify(self, person1, person2):    
        """identify person1 and person2
        
        arguments:
            person1, person2 - instances of Person
        returns:
            a Person instance - representing the identified person
        """
        
        #we need to merge the two persons, and choose one as the one to "point to"
        #we take the one that uses a biography with the highest trusworthiness
        
        trust1 = max([bio.get_source().quality for bio in person1.get_biographies() if bio.get_source().id != 'bioport'] )
        trust2 = max([bio.get_source().quality for bio in person2.get_biographies() if bio.get_source().id != 'bioport'] )
       
        if trust1 > trust2:
            new_person = person1
            old_person = person2
        else:
            new_person = person1
            old_person = person2
        #find out which one is the oldest
#        timestamp1 = self.get_session().query(BioPortIdRecord.timestamp).filter(BioPortIdRecord.bioport_id==person1.get_bioport_id()).one()
#        timestamp2 = self.get_session().query(BioPortIdRecord.timestamp).filter(BioPortIdRecord.bioport_id==person2.get_bioport_id()).one()
#        
#        if timestamp1[0] is None:
#            new_person = person1
#            old_person = person2
#        elif timestamp2[0] is None:
#            new_person = person2
#            old_person = person1
#        elif timestamp1 < timestamp2:
#            new_person = person1
#            old_person = person2
#        else:
#            new_person = person2
#            old_person = person1
#        
        if new_person.bioport_id == old_person.bioport_id:
            #these two persons are already identified
            return new_person
        
        #changhe de bioportid table
        self.redirect_identifier(old_person.get_bioport_id(), new_person.get_bioport_id())
            
        #now attach all biographies to the new bioportid
        for bio in new_person.get_biographies() + old_person.get_biographies(): 
            bio.set_value('bioport_id',new_person.get_bioport_id())
            self.save_biography(bio)

        for bio in old_person.get_biographies(): 
            new_person.add_biography(bio)
         
        #if we have different bioport biographies, we need to choose one
        new_id = new_person.bioport_id
        old_id = old_person.bioport_id
        #adapt the caches
        #we identified so we can remove this pair from the deferred list
        self._remove_from_cache_deferidentification(new_person, old_person)  
        self._update_similarity_cache_with_identification(new_id, old_id )
       

        #now delete the old person from the Person table
        self.delete_person(old_person)
        
        return new_person 

    def _update_similarity_cache_with_identification(self, new_id, old_id ):
        #update the similarity cache replaceing the old bioport_id with the new one
        session = self.get_session()
        qry = session.query(CacheSimilarityPersons)
        qry = qry.filter(or_(CacheSimilarityPersons.bioport_id1 == old_id, CacheSimilarityPersons.bioport_id2 == old_id))
        #we have to do it record by record, because we may be creating duplicates
        ls = list(qry.all())
        for r in ls:
            if r.bioport_id1 == old_id and r.bioport_id2 == old_id:
                session.delete(r)
                session.commit()
                continue
            
            if r.bioport_id1 == old_id:
                bioport_id1 = new_id
                bioport_id2 = r.bioport_id2
            else:
                bioport_id1 = r.bioport_id1 
                bioport_id2 = new_id
            if bioport_id1 > bioport_id2: 
                bioport_id1, bioport_id2 = bioport_id2, bioport_id1
                
            try:
                r.bioport_id1 = bioport_id1
                r.bioport_id2 = bioport_id2
                session.commit()
            except IntegrityError:
                #this thing was already in the database; we keep the one with the highest score
                session.rollback()
                other_r = self.get_session().query(CacheSimilarityPersons).filter_by(bioport_id1=bioport_id1, bioport_id2=bioport_id2).one()
                if other_r.score > r.score:
                    session.delete(r)
                else:
                    session.delete(other_r)
                    session.commit()
                    r.bioport_id1 = bioport_id1
                    r.bioport_id2 = bioport_id2
                session.commit()
        assert not qry.count(), [(r.bioport_id1, r.bioport_id2) for r in qry.all()]
               
    def unidentify(self, person):
        """Create a new person for each biography associated with person.
        """
        bios = person.get_biographies()
        result = []
        if len(bios) == 1:
            return [person]
        
        self.delete_person(person)
        used_ids = []
        #print '0:', bios
        for bio in bios:
            if bio.get_source().id == 'bioport':
                #XXX what do we do with bioport biographies?
                #either we copy and add htem to all, or we delete them all
                #now we delete
                self.delete_biography(bio)
            else:
                original_bioport_id = bio.get_idnos(type='bioport')[0]
                #print '1:',  original_bioport_id
                #the next three lines are there only because in a previous version, bioport_ids were not 'remembered 
                if original_bioport_id in used_ids:
                    original_bioport_id = self.fresh_identifier()
                used_ids.append(original_bioport_id)
                #print used_ids
                #save the changes to the biography
                bio.set_value('bioport_id',original_bioport_id)
                self.save_biography(bio)
                
                #remove the 'redirect' instruction from this bioport id (if there was one)
                self.redirect_identifier(bioport_id=original_bioport_id, redirect_to=None)
                
                #create a new person
                new_person = Person(bioport_id=original_bioport_id, biographies=[bio])
                new_person.repository = self
                new_person.add_biography(bio)
                self.save_person(new_person)
                result.append(new_person) 
        return result

                   
    def antiidentify(self, person1, person2):
        """register the fact that the user thinks that these two persons are not the same"""
        session = self.get_session()
        id1, id2 = person1.get_bioport_id(), person2.get_bioport_id()
        
        #add a witness record to the antiidentify table
        r_anti = AntiIdentifyRecord(bioport_id1 = min(id1, id2),bioport_id2= max(id1, id2)) 
        try:
            session.add(r_anti)
            msg = 'Anti-identified %s and %s' % (id1, id2)
            self.log(msg, r_anti)
            session.commit()
        except IntegrityError: 
            #this is (most probably) because the record already exists 
            session.rollback()
            pass
       
        self._remove_from_cache_similarity_persons(person1, person2)
        self._remove_from_cache_deferidentification(person1, person2)


    def _remove_from_cache_deferidentification(self, person1, person2):
        #remove the persons from the "deferred" lists if they are there
        session = self.get_session()
        id1 = person1.get_bioport_id()
        id2 = person2.get_bioport_id()
        qry = session.query(DeferIdentificationRecord) 
        qry = qry.filter(DeferIdentificationRecord.bioport_id1==min(id1, id2))
        qry = qry.filter(DeferIdentificationRecord.bioport_id2==max(id1, id2))
        qry.delete()
        
        #commit the changes
        session.commit()
        
    def _remove_from_cache_similarity_persons(self, person1, person2):
        #also remove the person  from the cache
        session = self.get_session()
        id1 = person1.get_bioport_id()
        id2 = person2.get_bioport_id()
        qry = session.query(CacheSimilarityPersons)
        qry = qry.filter(CacheSimilarityPersons.bioport_id1 == min(id1, id2))
        qry = qry.filter(CacheSimilarityPersons.bioport_id2 == max(id1, id2))
        qry.delete()        
        session.commit()
        
    def get_antiidentified(self):
        query = self.get_session().query(AntiIdentifyRecord)
        return query.all()
    
    def get_identified(self, **args):
        """what we really want is the "canonical" ids of the persons that have been identified
        (not the ones that are redirecting to others, as we have now)
        """
        return self.get_persons(is_identified=True, **args)
        
        session = self.get_session()
        qry = session.query(
            BioPortIdRecord
            )
#       qry = self._get_persons_query(**args)
#       qry = qry.join(BioPortIdRecord)
        qry = qry.filter(BioPortIdRecord.redirect_to != None)
            
        return qry.all()
        
    def defer_identification(self, person1, person2): 
        """register the fact that the user puts this pair at the "deferred  list """
        id1, id2 = person1.get_bioport_id(), person2.get_bioport_id()
        session = self.get_session()
        
        r_defer = DeferIdentificationRecord(bioport_id1 = min(id1, id2),bioport_id2= max(id1, id2)) 
        try:
            session.add(r_defer)
            msg = 'Deferred identification of %s and %s' % (id1, id2)
            self.log(msg, r_defer)
            session.commit()
        except IntegrityError: 
            session.rollback()
            #this is (most probably) because the record already exists 
            pass
        
        #also remove the persons from the cache
        self._remove_from_cache_similarity_persons(person1, person2)
        
    def get_deferred(self):
        qry = self.get_session().query(DeferIdentificationRecord)
        qry = qry.filter(DeferIdentificationRecord.bioport_id1 !=DeferIdentificationRecord.bioport_id2)
        return qry.all()
    
    
    #### LOCATIONS ######
    def _update_geolocations_table(self, limit=-1):
        from geolocations import refill_geolocations_table
        this_dir = os.path.dirname(__file__)
        source_fn = os.path.join(this_dir, 'geografische_namen', 'nl.txt')
        refill_geolocations_table(source_fn=source_fn, session=self.get_session(), limit=limit)
        
    
    def get_locations(self, name=None, startswith=None, order_by='sort_name'):
        qry = self.get_session().query(Location)
        if order_by:
            qry = qry.order_by('sort_name')
        if name:
            qry = qry.filter(Location.full_name == name)
        elif startswith:
            qry = qry.filter(Location.sort_name.startswith(startswith))
            
        return qry.all() 
    
    #### OCCUPATIONS #####
    def _update_occupations_table(self):
        from occupations import fill_occupations_table
        self.metadata.create_all()
        fill_occupations_table(self.get_session())
      
    def get_occupations(self):
        qry = self.get_session().query(Occupation)
        return qry.all()
    
    def get_occupation(self,id):
        qry = self.get_session().query(Occupation).filter(Occupation.id==id)
        return qry.one()
    #### RUBRIEKEN ####
    def _update_category_table(self):
        from categories import fill_table
        self.metadata.create_all()
        fill_table(self.get_session())
      
    def get_categories(self):
        qry = self.get_session().query(Category)
        return qry.all()
    
    def get_places(self, place_type=None):
        """ Get all places from the database.
            If place_type is either 'sterf' or 'geboorte' it will only
            return death or birth places.
        """
        col_geboorte = PersonRecord.geboorteplaats.label('plaats')
        col_sterf = PersonRecord.sterfplaats.label('plaats')
        select = sqlalchemy.sql.expression.select
        geboorte_query = select([col_geboorte]).where(
            col_geboorte != None).distinct()
        sterf_query = select([col_sterf]).where(
            col_sterf != None).distinct()
        if place_type and place_type in ('sterf', 'geboorte'):
            if place_type == 'sterf':
                query = sterf_query
            elif place_type == 'geboorte':
                query = geboorte_query
        else:
            query = geboorte_query.union(sterf_query)
        query = query.order_by('plaats')
        session = self.get_session()
        results = session.execute(query).fetchall()
        return [el[0] for el in results]

    
    def get_category(self,id):
        qry = self.get_session().query(Category).filter(Category.id==id)
        try:
            return qry.one()
        
        except NoResultFound:
            msg =  'No category with id "%s" could be found' % id
#            raise Exception(msg)
            LOG('BioPort', WARNING,msg) 
    
    def get_log_messages(self, table=None, user=None, order_by='timestamp', order_desc=True):
        qry = self.get_session().query(ChangeLog)
        if table:
            qry = qry.filter(ChangeLog.table==table)
        if user:
            qry = qry.filter(ChangeLog.user==user)
        if order_by:
            if order_desc:
                qry = qry.order_by(sqlalchemy.desc(order_by))
            else:
                qry = qry.order_by(order_by)
            
        ls = qry.all()      
        
        return ls
        
    
    def log(self, msg, record, user=None):
        """write information abut the changed record to the log
        
        arguments:
            msg - a string
            record - any Table instance
            user - optional - a string
        
        NOTE:
            does not commit
        """
        if user is None: 
            user = self.user
            
        r = ChangeLog()
        r.user = user
        r.msg = msg
        dir(ChangeLog.metadata)
        r.table = record.__tablename__ 
        if hasattr(record, 'id'):
            id = record.id
        elif hasattr(record, 'bioport_id'):
            id = record.bioport_id
        else:
            id = None
#            assert 0, 'This record %s has no "id" or "bioport_id" column defined'  % record
        if type(id) == type(0):
            r.record_id_int = id
        else:
            r.record_id_str = id
        self.get_session().add(r)
    
    def get_comments(self, bioport_id):
        return self.get_session().query(Comment).filter(Comment.bioport_id==bioport_id)
    def add_comment(self, bioport_id, values):
        comment = Comment(**values)
        comment.created = datetime.now()
        self.get_session().add(comment)

        
    def get_persons_with_identical_dbnl_ids(self, start=0, size=20, refresh=False, source=None):
        session = self.get_session() 
        sql = """SELECT  SQL_CALC_FOUND_ROWS c.bioport_id1, c.bioport_id2, c.source1, c.source2, c.dbnl_id
        FROM dbnl_ids c 

LEFT OUTER JOIN antiidentical a
on 
    a.bioport_id1 =  c.bioport_id1
AND a.bioport_id2 = c.bioport_id2
LEFT OUTER JOIN defer_identification d
on 
    d.bioport_id1 =  c.bioport_id1
AND d.bioport_id2 = c.bioport_id2
LEFT OUTER JOIN
     bioportid b 
ON 
b.bioport_id = c.bioport_id1 and b.redirect_to = c.bioport_id2
LEFT OUTER JOIN
     bioportid b2
ON 
b2.bioport_id = c.bioport_id2 and b2.redirect_to = c.bioport_id1

WHERE 
c.bioport_id1 != c.bioport_id2 /*different persones */
and a.bioport_id1 is null /* not antiidentical */ 
and a.bioport_id2 is null
and d.bioport_id1 is null /*not deferred */ 
and d.bioport_id2 is null
and b.bioport_id is null /* not redirected to others */
and b.redirect_to is null
and b2.bioport_id is null /* not redirected to others */
and b2.redirect_to is null
        """
        if source:
            sql += ' AND c.source1 ="%s"  and c.source2="%s"' % (source, source)
        
        sql += ' ORDER BY c.dbnl_id'
        
        sql += ' LIMIT %s OFFSET %s' % (size, start)
        rs = session.execute(sql)
        grand_total = list(session.execute("select FOUND_ROWS()"))[0][0]
        return ([(Person(r.bioport_id1, repository=self), Person(r.bioport_id2, repository=self)) for r in rs], grand_total)


    def tmp_fixup_category_doublures(self):
        """cleanup after a bug that assigned double categories to persons
        
        this method can be removed when it is not useful anymore """
        
        for person in self.get_persons():
            ls = self.get_biographies(source='bioport', person=person)
            if not ls:
                continue
            bio = ls[0] 
            used_ids = [state.get('idno') for state in bio.get_states(type='category')]
            #check if useD_ids has doubles
            if len(set(used_ids)) != len(used_ids):
                used_ids = list(set(used_ids))
                bio.set_category(used_ids)
                self.save_biography(bio)
        print 'DONE tmp_fixup_category_doublures'

    def tmp_identify_misdaad_recht(self):
        """identify the categories "misdaad" en "recht" in the whole database
        
        this method can be removed when it does not seem useful anymore 
        """
        #misdaad = 9
        #rechts = 13
        for person in self.get_persons(category=13):
            ls = self.get_biographies(source='bioport', person=person) 
            for bio in ls:
                print bio
                for state in bio.get_states(type='category'):
                    if state.get('idno') == '13':
                        state.set('idno', '9')
                        self.save_biography(bio)
        print 'DONE tmp_identify_misdaad_recht'     
        
    def tmp_fix_weird_categeries(self, bio=None):
        """fixing errors in category assignment - this method can be removed when it does not seem necessary anymore"""
        if bio:
            bios = [bio]
        else:
            bios =  self.get_biographies(source='bioport')
        i = 0
        for bio in bios:
            i += 1
            states =  bio.get_states(type='category')
            for state in states:
                idno = state.get('idno')
                if not idno.isdigit():
                    print i
                    print idno
                    idnos = eval(idno)
                    idnos = list(idnos)
                    used_ids = [idno for idno in [state.get('idno') for state in states] if idno.isdigit()]
                    idnos = used_ids + idnos
                    if '13' in idnos:
                        idnos.remove('13')
                        idnos.append('9')
                    idnos = list(set(idnos)) 
                    print idnos
                    bio.set_category(idnos)
                    self.save_biography(bio)
                    break
                    
        print 'DONE!'

    def tmp_give_blnps_a_category(self):
        for p in self.get_persons(source_id='blnp'):
            bio = p.get_bioport_biography()
            categories =bio.get_states(type='category')
            categories = [c.get('idno') for c in categories]
            bio.set_category(categories + [4])
            self.save_biography(bio)
