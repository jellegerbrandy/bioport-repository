from sqlalchemy import Column, Integer, Unicode,String, ForeignKey,  Boolean, UnicodeText, Float, BLOB
from sqlalchemy import create_engine, MetaData, Text, desc, and_, or_, not_, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.databases.mysql import MSString
from sqlalchemy.orm import relation #, backref, eagerload, aliased
#from sqlalchemy.orm.query import Query

from sqlalchemy.types import TIMESTAMP

#define the tables

metadata = MetaData()
Base = declarative_base()


class BiographyRecord(Base):
    __tablename__ = 'biography'

    #db_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(MSString(50, binary=True, collation='utf8_bin'), primary_key=True, index=True, unique=True,) #the id consist of source_id/local_id
    source_id = Column(MSString(50, collation='utf8_bin'), ForeignKey("source.id"),index=True)
#    local_id = Column(MSString(50), index=True,  nullable=False)
    biodes_document = Column(Text(64000))
    source_url = Column(Unicode(255)) #the url where the biodes_document came from
    timestamp = Column(TIMESTAMP)
    
#    sqlalchemy.schema.ForeignKeyConstraint(['id'], ['naam.biography_id'], ondelete="CASCADE") 
    authors = relation( 'RelBiographyAuthorRecord') #, cascade="all, delete, delete-orphan", backref='biography')
    bioportid = relation('RelBioPortIdBiographyRecord')
    hide = Column(Boolean)

#    bioport_id_records = relation('BioPortIdRecord')
    
    def get_bioport_id(self):
        return self.bioportid[0].bioport_id
    
class SourceRecord(Base):
    __tablename__ = 'source'
#    db_id = Column(Integer,primary_key=True, autoincrement=True)
    id = Column(MSString(50), index=True,primary_key=True)
    url = Column(MSString(255))
    description = Column(MSString(255), nullable=True)
    quality = Column(Integer)
    xml = Column(Text(64000))
    timestamp = Column(TIMESTAMP)
#    sqlalchemy.schema.ForeignKeyConstraint(['id'], ['biography.source_id'], ondelete="CASCADE")
    
    def __init__(self, id, url, description, quality=None, xml=None):
        self.id = id
        self.url = url
        self.description = description
        self.quality = quality
        self.xml=xml
 
#
# NOTA BENE:
#    The tables are not normalized completely.
#    The reason is that the data in the bioportid table needs to be persistent
#    while the data of the biography table in general is not
#
# 

class BioPortIdRecord(Base):
    __tablename__ = 'bioportid'
    bioport_id = Column(MSString(50), ForeignKey("bioportid.bioport_id"), primary_key=True)
    redirect_to = Column(MSString(50)) 
    timestamp = Column(TIMESTAMP)
    biographies = relation('RelBioPortIdBiographyRecord')
    person = relation('PersonRecord')
    
class RelBioPortIdBiographyRecord(Base):
    __tablename__ = 'relbioportidbiography'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bioport_id = Column(MSString(50), ForeignKey('bioportid.bioport_id'),index=True)
    biography_id = Column(MSString(50, collation='utf8_bin'), ForeignKey("biography.id"),index=True, unique=True)
    timestamp = Column(TIMESTAMP)
    biography = relation(BiographyRecord) 
    bioportid = relation(BioPortIdRecord)
    
class AuthorRecord(Base):   
    """XXX the author table serves as a cache and since we mostly look for persons,
    it makes sense to make the relation with the person table directly"""
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(MSString(255), nullable=False, unique=True) 
    biographies = relation( 'RelBiographyAuthorRecord', cascade="all, delete-orphan")
    
class RelBiographyAuthorRecord(Base):
    __tablename__ = 'relbiographyauthor'
    biography_id = Column(MSString(50, collation='utf8_bin' ),  ForeignKey('biography.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), primary_key=True) 
    author = relation(AuthorRecord,cascade='all') 
#    biography = relation(BiographyRecord, cascade='all,delete')
#    sqlalchemy.schema.ForeignKeyConstraint(['author_id'], ['author.id'], ondelete="CASCADE, ALL") 
#    sqlalchemy.schema.ForeignKeyConstraint(['biograpy_id'], ['biography.biography_id'], ondelete="CASCADE")
    

class SoundexRecord(Base):
    __tablename__ = 'soundex'
    id = Column(Integer,primary_key=True)
    naam_id = Column(Integer, ForeignKey('naam.id'))
    soundex  = Column(Unicode(100))

    
class PersonRecord(Base):
    """This is basically a 'cache' table for searching for persons in the database, together with some meta-data
    
    The data are a combination of the data from the biographies associated with a bioport id
    """
    
    __tablename__ = 'person'

    #db_id = Column(Integer, primary_key=True, autoincrement=True)
#    id = Column(Integer, primary_key=True, auto_increment=True)
    bioport_id = Column(
        MSString(50), 
        ForeignKey('bioportid.bioport_id'), 
        primary_key=True,
        index=True, 
        unique=True,
        )
    geboortedatum = Column(MSString(10), index=True)
    geboortejaar = Column(Integer, index=True)
    geboorteplaats = Column(MSString(255), index=True)
    sterfdatum = Column(MSString(10), index=True)
    sterfjaar = Column(Integer, index=True)
    sterfplaats = Column(MSString(255), index=True)
    naam = Column(MSString(255), index=True)
    geslachtsnaam = Column(MSString(255), index=True)
    names = Column(UnicodeText)
    sort_key = Column(MSString(50), index=True)
    sex = Column(Integer, index=True)
    bioport_id_record = relation(BioPortIdRecord)
    
#    sqlalchemy.schema.ForeignKeyConstraint(['bioport_id'], ['bioportid.bioport_id'])
    search_source = Column(UnicodeText)
    snippet = Column(UnicodeText)
    remarks = Column(UnicodeText)
    thumbnail = Column(MSString(255))
    status = Column(Integer, index=True)
    
    has_illustrations = Column(Boolean)
    
    timestamp = Column(TIMESTAMP)
#    categories = relation('RelPersonCategory') #this propertie is already defined by backref on RelPresonCategory

class PersonSoundex(Base): 
    __tablename__ = 'person_soundex'
    id = Column(Integer, primary_key=True)
    bioport_id = Column(MSString(50),ForeignKey('person.bioport_id'), index=True, )
    soundex = Column(Unicode(20), index=True)
    
class PersonName(Base): 
    __tablename__ = 'person_name'
    id = Column(Integer, primary_key=True)
    bioport_id = Column(MSString(50),ForeignKey('person.bioport_id'), index=True, )
    name = Column(Unicode(20), index=True)
    
class PersonSource(Base):     
    __tablename__ = 'person_source'
    id = Column(Integer, primary_key=True)
    bioport_id = Column(MSString(50),ForeignKey('person.bioport_id'), index=True, )
    source_id = Column(Unicode(20), index=True)
    
class NaamRecord(Base):
    __tablename__ = 'naam'
    id = Column(Integer,primary_key=True)
    
    soundex = relation(SoundexRecord) #, backref="naam.id")
    sort_key = Column(Unicode(100))
    snippet = Column(UnicodeText)
    birth = Column(Unicode(10))
    death = Column(Unicode(10))
    url = Column(Unicode(255))
    src = Column(Unicode(255))
    xml = Column(UnicodeText)
    volledige_naam = Column(Unicode(255))
    url_description = Column(UnicodeText)
    territoriale_titel = Column(Unicode(255))
    variant_of = Column(Integer, ForeignKey('naam.id') )
    varianten = relation("NaamRecord") 
    variant_of_record = relation("NaamRecord",
             remote_side="NaamRecord.id",
             )
    bioport_id = Column(MSString(50), ForeignKey('person.bioport_id'), index=True)
    person = relation(PersonRecord, 
                         lazy=False, #load eagerly
                         )
#    sqlalchemy.schema.ForeignKeyConstraint(['id'], ['soundex.naam_id'], ondelete="CASCADE")
        
class SimilarityCache(Base):
    __tablename__ = 'cache_similarity' 
    naam1_id = Column(Integer, ForeignKey('naam.id'), index=True, primary_key=True, autoincrement=False)
    naam2_id = Column(Integer, ForeignKey('naam.id'), index=True, primary_key=True, autoincrement=False)
    score = Column(Float, index=True) 
SimilarityCache.naam1 = relation(NaamRecord, primaryjoin=NaamRecord.id ==SimilarityCache.naam1_id) 
SimilarityCache.naam2 = relation(NaamRecord, primaryjoin=NaamRecord.id ==SimilarityCache.naam2_id)

class CacheSimilarityPersons(Base):
    __tablename__ = 'cache_similarity_persons' 
    bioport_id1 = Column(MSString(50), ForeignKey('bioportid.bioport_id'), index=True, primary_key=True, autoincrement=False)
    bioport_id2 = Column(MSString(50), ForeignKey('bioportid.bioport_id'), index=True, primary_key=True, autoincrement=False)
    score = Column(Float, index=True) 
    
class AntiIdentifyRecord(Base):    
    __tablename__ =  'antiidentical'
    bioport_id1 = Column(MSString(50), 
                        ForeignKey('bioportid.bioport_id'), 
                        primary_key=True)
    bioport_id2 = Column(MSString(50), 
                        ForeignKey('bioportid.bioport_id'), 
                        primary_key=True)
    
    timestamp = Column(TIMESTAMP)
    
class DeferIdentificationRecord(Base):
    __tablename__ =  'defer_identification'
    bioport_id1 = Column(MSString(50), 
                        ForeignKey('bioportid.bioport_id'), 
                        primary_key=True)
    bioport_id2 = Column(MSString(50), 
                        ForeignKey('bioportid.bioport_id'), 
                        primary_key=True)
    timestamp = Column(TIMESTAMP)
    timestamp = Column(TIMESTAMP)


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True,  autoincrement=True)
    ufi = Column(Integer)
    uni = Column(Integer)
    long = Column(Float)
    lat = Column(Float)
    adm1 = Column(MSString(2), index=True)
    sort_name=Column(MSString(100), index=True)
    full_name=Column(MSString(100), index=True) #
    
    
    """
NL.00    Netherlands (general)
NL.01    Provincie Drenthe
NL.02    Provincie Friesland
NL.03    Gelderland
NL.04    Groningen
NL.05    Limburg
NL.06    North Brabant
NL.07    North Holland
NL.09    Utrecht
NL.10    Zeeland
NL.11    South Holland
NL.15    Overijssel
NL.16    Flevoland
"""
    provinces= {
        '00':'Netherlands (general)',
		'01':'Drenthe',
		'02':'Friesland', 
		'03':'Gelderland', 
		'04':'Groningen', 
		'05':'Limburg', 
		'06':'Noord Brabant', 
		'07':'Noord Holland', 
		'09':'Utrecht', 
		'10':'Zeeland', 
		'11':'Zuid Holland', 
		'15':'Overijssel', 
		'16':'Flevoland', 
        }
    def province(self):
        return self.provinces[self.adm1]
    
class Occupation(Base):
    __tablename__ = 'occupation'
    id = Column(Integer, primary_key=True)
    name=Column(MSString(100), index=True) # *   
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name=Column(MSString(100), index=True) # *      
    
class ChangeLog(Base):
    __tablename__  = 'changelog'
    id = Column(Integer, primary_key=True)
    table = Column(MSString(50), index=True)
    record_id_int = Column(Integer, index=True)
    record_id_str = Column(MSString(255), index=True)
    msg = Column(Text)
    user = Column(MSString(50))
    timestamp = Column(TIMESTAMP)


class DBNLIds(Base):
    """this is a temporary class used for identifying vdaa and nnbw entries"""
    __tablename__ = 'dbnl_ids' 
    bioport_id1 = Column(MSString(50), ForeignKey('bioportid.bioport_id'), index=True, primary_key=True, autoincrement=False)
    bioport_id2 = Column(MSString(50), ForeignKey('bioportid.bioport_id'), index=True, primary_key=True, autoincrement=False)
    source1 = Column(MSString(5))
    source2 = Column(MSString(5))
    dbnl_id = Column(MSString(20))
    score = Column(Float, index=True) 
 
class RelPersonCategory(Base):
    __tablename__ = 'relpersoncategory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bioport_id = Column(Integer, ForeignKey('person.bioport_id'), index=True)
    category_id = Column(Integer, ForeignKey('category.id'), index=True)   
    persons = relation(PersonRecord, backref='categories')
    
    
    
class Comment(Base):
    """This table holds comments submitted by portal users
    """
    
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bioport_id = Column(
                        MSString(50), 
                        ForeignKey('bioportid.bioport_id'), 
                        index=True, 
                        unique=True,
                        )
    text = Column(Text)
    created = Column(DateTime, index=True)
    submitter = Column(MSString(20), default='Anonymous')
    email = Column(MSString(40))
    
STATUS_NEW = 1
STATUS_VALUES =  [
    (STATUS_NEW, 'nieuw'), #
    (2, 'bewerkt'),
    (12, 'nog niet bewerkt'),
    (3, 'moeilijk geval'),
    (5, 'moeilijk geval (troep)'),
    (4, 'klaar'), 
    (7, 'te weinig informatie'), 
    (8, 'familielemma'), 
    (9, 'verwijslemma'), 
    (10, 'nader onderzoek nodig'), 
    (11, 'buitenlands'), 
    (13, 'portrait'), 
    (0, '(geen status toegekend)'),
]
