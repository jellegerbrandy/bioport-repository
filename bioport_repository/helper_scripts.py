from bioport_repository.repository import Repository
from bioport_repository.db_definitions import  CacheSimilarityPersons
DSN ='mysql://localhost/bioport'
LIMIT = 0

"""

USAGE:
from bioport_repository.helper_scripts import _remove_irrelevent_items_from_similarity_table
dsn = 'mysql://localhost/bioport'
_remove_irrelevent_items_from_similarity_table(dsn)
"""

def _remove_irrelevent_items_from_similarity_table(dsn):
    repository = Repository(db_connection=dsn)
    db = repository.db
    session = db.get_session() 
    qry = session.query(CacheSimilarityPersons)
    i = 0 
    j = 0
    k = 0
    total = qry.count()
    for r in qry:
        i += 1
        print 'progress %s/%s' % (i, total)
        try:
            if not db._should_be_in_similarity_cache(r.bioport_id1, r.bioport_id2):
                print 'deleting %s form similiaryt cache' % r
                j += 1
                k += 1
                session.delete(r)
                session.commit()
        except Exception, error:
            print error
            session.rollback()
    session.commit()
    print 'deleted %s items' % j 
    print 'committing...'
    print 'done.'
 
"""
USAGE:
    
from bioport_repository.helper_scripts import identify_dbnl_biographies
dsn = 'mysql://localhost/bioport'
identify_dbnl_biographies(dsn)
"""
def identify_dbnl_biographies(dsn):
    """search in the database for all biographies that have an idno of type 'dbnl_id'
       and identify all persons that have the same dbnl_id
    """
    repository = Repository(db_connection=dsn)
    #create a dictionary of all dbnl_ids and corresponding bioport_ids
    dct = {}
    def get_bios():
        for source_id in ['dbnl', 'nnbw', 'vdaa']:
            for biography in repository.get_biographies(source=source_id):
                yield biography
    
    i = 0
    for biography in get_bios():
        i += 1
        print i
        if LIMIT and i > LIMIT:
            break
        dbnl_id = biography.get_idno(type='dbnl_id')
        if dbnl_id and dbnl_id not in ['None']:
            bioport_id = biography.get_bioport_id()
            if bioport_id not in dct.get(dbnl_id, []):
                dct[dbnl_id] = dct.get(dbnl_id, []) + [bioport_id]
    for k in dct.keys():
        if len(dct[k]) < 2:
            del dct[k]
    total = len(dct)
    i = 0
    for dbnl_id in dct:
        i += 1
        print '%s/%s' % (i, total)
        bioport_ids = dct[dbnl_id]
        bioport_id1 = bioport_ids[0]    
        person1 = repository.get_person(bioport_id1)
        for bioport_id2 in bioport_ids[1:]:
            person2 = repository.get_person(bioport_id2)
            print 'identifying', person1, person2
            if person1 and person2: #this to avoid a misterious bug that i cannot be bothered to investiage
                if not repository.is_antiidentified(person1, person2):
                    person1 = repository.identify(person1, person2)
            else:
                person1 = person2
        person1 = person2 = None
            
        
        

if __name__ == '__main__':
    identify_dbnl_biographies(dsn=DSN)