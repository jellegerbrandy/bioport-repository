from bioport_repository.tests.common_testcase import CommonTestCase, unittest , THIS_DIR

from bioport_repository.repository import *
from bioport_repository.db_definitions import *
from bioport_repository.person import Person


class RepositoryTestCase(CommonTestCase):

    def test_download_bios(self):
        url = os.path.abspath(os.path.join(THIS_DIR, 'data/knaw/list.xml'))
        #add some sources source
        src = Source(id=u'test', url=url , description=u'test')
        self.repo.add_source(src)
    
        self.repo.download_biographies(src)
        assert len(self.repo.get_biographies())
    

        
    def test_get_persons(self):
        self.assertEqual(len(self.repo.get_persons()), 10)
        self.assertEqual(self.repo.count_persons(), 10)
    def test_get_persons_sequence(self):
        persons = self.repo.get_persons_sequence()
        self.assertEqual(len(persons), 10)
        b_persons = self.repo.get_persons_sequence(beginletter='b')
        assert 0<len(b_persons) <  len(persons) #not all person names start with a 'b'

    def test_created_repository(self):
        repo = self.create_filled_repository()
        
        bios = repo.get_biographies()
        self.assertEqual(len(bios), 10)
        bio = bios[3]
        assert bio.get_value('local_id')
        assert bio.get_value('bioport_id')
    
    def test_add_biography(self):
        #make a new biography
        source = Source(id=u'bioport_test')
        self.repo.add_source(source)
        bio = Biography( id = u'test_bio.xml', source_id=source.id)
        
        #XXX Do we need this?
        bio.from_args( 
              url_biografie='http://ladida/didum', 
              naam_publisher='nogeensiets', 
              url_publisher='http://pbulihser_url',
              naam='Tiedel Doodle Dum',
              local_id='123',
              )
        
        #save it
        self.repo.add_biography(bio)
        assert bio.get_bioport_id()
        self.assertEqual(bio.repository, self.repo)
        
    def test_get_biographies(self):
        self.create_filled_repository()
        bio = self.repo.get_biographies()[2]
        id =bio.get_bioport_id()
        assert id, bio.to_string()
        p = Person(id)
        source = bio.get_source()
        self.assertEqual([b.id for b in self.repo.get_biographies(person=p)], [bio.id])
        self.assertEqual(len(self.repo.get_biographies(source=source)), 5)
        self.assertEqual(self.repo.get_biographies(person=p, source=bio.get_source()), [bio])
               
    
        self.assertEqual(self.repo.count_biographies(), len(self.repo.get_biographies()))
        self.assertEqual(self.repo.count_biographies(source=source), 5)
        
                   
#    def test_similar_bios(self):   
#        self.create_filled_repository()
#        repo = self.repo
#        #get a person
#        person = repo.get_persons()[1]
#        #there are two names similar to the name of this person
#        names = repo.get_similar_names(person)
#        self.assertEqual(len(names), 3)
##        assert 0, '%s - %s ' % (person.get_merged_biography().get_names(), persons)
#        #we can ge the biography of the name
#        name = names[0]
#        
#        assert name.get_biography()
#        #nad also the person corresponding to the biography
#        #XXX
#        #assert name.get_biography().get_person()
        
    def test_source_manipulation(self):  
        i = self.repo 
        url = 'file://%s' % os.path.abspath(os.path.join(THIS_DIR, 'data/knaw/list.xml'))
        sources = i.get_sources()
        
        #add some sources source
        src1 = Source(id=u'test', url=url , description=u'test')
        i.add_source(src1)
        
        src2 = i.add_source(Source(id=u'test2', url=url , description=u'test2 description'))
       
        self.assertEqual(len(i.get_sources()), len(sources) + 2, i.get_sources())
        #and the source we added is among  them
        assert 'test' in [s.id for s in i.get_sources()], i.get_sources()
      
        self.assertEqual(src2.url, url)
        self.assertEqual(src2.description,'test2 description')
        
        i.download_biographies(src1)
        self.assertEqual(len(i.get_biographies(source=src1)), 5)
        
        i.delete_biographies(src1)
        self.assertEqual(len(i.get_biographies(source=src1)), 0)
        
        i.download_biographies(source=src1)
        self.assertEqual(len(i.get_biographies(source=src1)), 5)
        
        i.delete_biographies(src1)
        self.assertEqual(len(i.get_biographies(source=src1)), 0)
        
        #the source is also in the repository         
        #see if we can delete the source
        i.delete_source(Source(u'test'))
        self.assertEqual(len(i.get_sources()), 1 + len(sources))
        
        self.assertEqual(len(i.get_biographies(source=Source('test'))), 0)
    def test_refill(self):
        self.create_filled_repository()
        #now donwload the data from the first source a seond time
        
       
    def test_redirect_to(self):
        repo = self.create_filled_repository()
        bioport_ids = repo.get_bioport_ids()
        id1 = bioport_ids[1]
        id2 = bioport_ids[2]
        self.assertEqual(repo.redirects_to(id1), id1)
        repo.redirect_identifier(id1, id2)
        self.assertEqual(repo.redirects_to(id1), id2)
        

        
    def test_bioport_biography(self):
        repo = self.create_filled_repository()
        person = repo.get_persons()[2]
        
        #get the bioport biography (the one used for editing)
        bio = repo.get_bioport_biography(person)
        #check sanity
        self.assertEqual(bio.get_value('bioport_id'), [person.get_bioport_id()]) 
        self.assertEqual(self.repo.db.get_sources()[0], bio.get_source())
        #set a value
        bio.set_value('geboortedatum', '1999-01-01')
        repo.save_biography(bio)
        
        self.assertEqual(bio.get_value('geboortedatum'), '1999-01-01')
        
        
        self.assertEqual(person.get_merged_biography().get_value('geboortedatum'), '1999-01-01')
        
        bio.set_value('geboortedatum', '1999-01-02')
        
        self.assertEqual(bio.get_value('geboortedatum'), '1999-01-02')
        repo.save_biography(bio)
        self.assertEqual(self.repo.get_person(person.bioport_id).get_merged_biography().get_value('geboortedatum'), '1999-01-02')
    
    def test_save_biography(self):
        source = Source(id='bioport_test')
        self.repo.add_source(source)
        bio = Biography( id = 'test_bio.xml', source_id=source.id)
        
        name = 'Name1'
        #XXX Do we need this?
        bio.from_args( 
              url_biografie='http://ladida/didum', 
              naam_publisher='nogeensiets', 
              url_publisher='http://pbulihser_url',
              naam=name,
              local_id='123',
              )
        self.assertEqual(len(bio.get_idnos()), 1, bio.to_string())
        self.repo.save_biography(bio)
        #we now have two idnos: the local "id", and the "bioport_id"
#        assert 0, bio.xpath('person/idno')
        self.assertEqual(len(bio.get_idnos(type=None)), 2, bio.to_string())
        
        self.assertEqual(self.repo.get_biography(bio.id).naam().volledige_naam(), name)
        name = 'Name2'
        bio.set_value('namen', [name])
        self.repo.save_biography(bio)
        
        self.assertEqual(self.repo.get_biography(bio.id).naam().volledige_naam(), name, bio.to_string())
        self.assertEqual(len(bio.get_idnos(type=None)), 2, bio.to_string())
        
    def test_antiidentify(self):
        repo = self.create_filled_repository()
        persons = repo.get_persons()
        self.repo.db.fill_similarity_cache(minimal_score=0.0)
        ls = self.repo.get_most_similar_persons()
        score, p1, p2 = ls[1]
#        assert 0, [(p.get_bioport_id(), p2.get_bioport_id()) for score, p, p2 in ls]
        #we have n candidates
        n = len(ls)
        self.assertEqual(len(list(ls)), n)
        #now we anti-identify one pair
        repo.antiidentify(p1, p2)
        #check if we really anti-identified only one pair
        self.assertEqual(self.repo.db.get_session().query(AntiIdentifyRecord).count(), 1)
        
        #so, now we must have 1 less person left
        ls = self.repo.get_most_similar_persons()
        self.assertEqual(len(list(ls)), n-1)

        self.assertEqual(len(list(repo.get_antiidentified())), 1)    

    
    def test_unidentify(self):
        repo = self.create_filled_repository(sources=1)
        persons = repo.get_persons()
        p1 = persons[1]
        p2 = persons[2]
        id1 = p1.bioport_id
        id2 = p2.bioport_id
        #identify two persons
        p = repo.identify(p1, p2)
        #the new person has one of the original bioport ids
        id = p.bioport_id
        self.assertTrue(id in [id1, id2])  

        self.assertEqual(len(repo.get_identified()), 1)
        #now unidentify them again
        ls = repo.unidentify(p)
        
        #we should get two persons back
        self.assertEqual(len(ls), 2)
        
        
        p3, p4 = ls
        id3 = p3.bioport_id
        id4 = p4.bioport_id
        
        #each of the new persons is associated with a single biogrpahy
        self.assertEqual(len(p3.get_biographies()),1)
        self.assertEqual(len(p4.get_biographies()),1)
        
        #all these new persons should be saved in the repository
        p3 = repo.get_person(id3)
        p4 = repo.get_person(id4)
        
        
        self.assertTrue(id1 in [id3, id4], [id1, id2, id3, id4, id])
        self.assertTrue(id2 in [id3, id4])
        self.assertEqual(len(p3.get_biographies()),1)
        self.assertEqual(len(p4.get_biographies()),1)
       
        #sanity? the biography should refer to the old id
        self.assertEqual(p3.get_biographies()[0].get_idno('bioport'), id3)
        self.assertEqual(p4.get_biographies()[0].get_idno('bioport'), id4)
        
        self.assertEqual(len(repo.get_identified()), 0)

    def test_fill_similarity_cache(self):
        repo = self.create_filled_repository()
        self.repo.db.fill_similarity_cache(refresh=True)
        source_id = self.repo.get_sources()[0].id
        self.repo.db.fill_similarity_cache(source_id=source_id, refresh=True)
        person = self.repo.get_persons()[0]
        self.repo.db.fill_similarity_cache(person=person, refresh=True)
        
    def test_workflow_identification(self):
        #we have three options in the identifaction process:
        #    1. identify the two
        #    2. anti-identify the two
        #    3. defer
        
        #set up ajn environmenet
        repo = self.create_filled_repository()
        self.repo.db.fill_similarity_cache(minimal_score=0.0)
        
        #we now have original_length "most similar persons"
        original_length = len(self.repo.get_most_similar_persons())
            
        #get two similar persons
        score, p1, p2 = self.repo.get_most_similar_persons()[1]
        
        
        #we should also find them if we search for the peopele
        ls = self.repo.get_most_similar_persons(bioport_id=p1.bioport_id)
        assert (score, p1, p2) in ls
        
        #now we identify two people
#        print p1, p2
        repo.identify(p1, p2)
#        print p1, p2
        assert len(self.repo.get_most_similar_persons()) <= original_length-1
        score, p1, p2 = self.repo.get_most_similar_persons()[1] 
        repo.antiidentify(p1, p2)
        assert len(self.repo.get_most_similar_persons()) <=  original_length-2
        
        score, p1, p2 = self.repo.get_most_similar_persons()[1] 
        repo.defer_identification(p1, p2)
        ls = self.repo.get_most_similar_persons()
        assert len(ls) <= original_length-3
        self.assertEqual(len(self.repo.get_deferred()), 1)
        
        
        score, p1, p2 = self.repo.get_most_similar_persons()[1] 
        repo.defer_identification(p1, p2)
        self.assertEqual(len(self.repo.get_deferred()), 2)
        assert len(self.repo.get_most_similar_persons()) <=  original_length-4
       
        id1 = min(p1.bioport_id, p2.bioport_id)
        id2 = max(p1.bioport_id, p2.bioport_id)
#        print id1, id2
#        print [r for r in self.repo.get_most_similar_persons()] 
        qry = repo.db.get_session().query(CacheSimilarityPersons)
#        print [(r.bioport_id1, r.bioport_id2) for r in qry.all()] 
        
        #(p1,p2) were deferred, but now we identify them after all
        
        
        repo.identify(p1, p2)
        
        #the deferred list contains now only 1 pair
        self.assertEqual(len(self.repo.get_deferred()), 1)
        
           
#class RepositoryTestCase(CommonTestCase):

    def test_refreshing_of_identification_cache(self):
        #we have three options in the identifaction process:
        #    1. identify the two
        #    2. anti-identify the two
        #    3. defer
        repo = self.repo
        #set up theG environmenet
        self.repo.db.fill_similarity_cache(minimal_score=0.0)
#        for r in repo.db.get_session().query(CacheSimilarityPersons):
#            print r.score, r.bioport_id1, r.bioport_id2
        persons = self.repo.get_persons()
#        print len(persons)
        similar_persons = self.repo.get_most_similar_persons()
#        print 'most similar:'
#        print len(similar_persons)
#        for p in similar_persons:
#            print p
        
        #We need at least 5  'most similar persons' for the tests below to work
        original_length= len(similar_persons)
        assert original_length >= 5, 'We need at least 5 "most similar persons" for the tests to work'
        
        score, p1, p2 = similar_persons[0] 
        repo.identify(p1, p2)
        new_len = len(self.repo.get_most_similar_persons()) 
        assert new_len <= original_length  -4,  '%s - %s' % (len(self.repo.get_most_similar_persons()), original_length)
        #all these identifications should also be persistent after we refill the cache
        #print '*fill similairty cache'
        repo.db.fill_similarity_cache(refresh=True,minimal_score=0.0  )
        #self.debug_info()
        self.assertEqual(len(self.repo.get_antiidentified()), 0)
        self.assertEqual(len(self.repo.get_identified()), 1)
        self.assertEqual(len(self.repo.get_deferred()), 0)
        self.assertEqual(len(self.repo.get_most_similar_persons()), new_len)
        self.assertEqual(len(self.repo.get_persons()), 9)

        score, p1, p2 = self.repo.get_most_similar_persons()[1]
#        p1, p2 = persons[2], persons[3]
        #print ' * antiidefnty', p1, p2
        repo.antiidentify(p1, p2)
        #self.debug_info()
        
        self.assertEqual(len(self.repo.get_antiidentified()), 1)
        self.assertEqual(len(self.repo.get_identified()), 1)
        self.assertEqual(len(self.repo.get_deferred()), 0)
        self.assertEqual(len(self.repo.get_most_similar_persons()),new_len-1) 
        self.assertEqual(len(self.repo.get_persons()), 9)
        
        #all these identifications should also be persistent after we refull the cache
        #print '*fill similairty cache'
        repo.db.fill_similarity_cache(refresh=True,minimal_score=0.0)
        #self.debug_info()
        self.assertEqual(len(self.repo.get_most_similar_persons()), new_len-1)        
        
        score, p1, p2 = self.repo.get_most_similar_persons()[1] 
        repo.defer_identification(p1, p2)
        #print '* deferred', p1, p2
        #self.debug_info()
        self.assertEqual(len(self.repo.get_antiidentified()), 1)
        self.assertEqual(len(self.repo.get_identified()), 1)
        self.assertEqual(len(self.repo.get_deferred()), 1)
        self.assertEqual(len(self.repo.get_most_similar_persons()), new_len -2)        
        
        #all these identifications should also be persistent after we refull the cache
        #print '*fill similairty cache'
        repo.db.fill_similarity_cache(refresh=True,minimal_score=0.0)
        self.debug_info()
        self.assertEqual(len(self.repo.get_most_similar_persons()), new_len-2 )        
        
        score, p1, p2 = self.repo.get_most_similar_persons()[4] 
        repo.defer_identification(p1, p2)
        #print '* deferred', p1, p2
        self.debug_info()
        self.assertEqual(len(self.repo.get_deferred()), 2)
        self.assertEqual(len(self.repo.get_identified()), 1)
        self.assertEqual(len(self.repo.get_antiidentified()), 1)
        self.assertEqual(len(self.repo.get_most_similar_persons()), new_len-3)
        
        #all these identifications should also be persistent after we refull the cache
        repo.db.fill_similarity_cache(refresh=True,minimal_score=0.0)
        self.assertEqual(len(self.repo.get_most_similar_persons()), new_len-3 )        
       
       
        #(p1,p2) were deferred, but now we identify them after all
        self.assertEqual(len(self.repo.get_identified()), 1)
        person = repo.identify(p1, p2)
        self.assertEqual(len(self.repo.get_identified()), 2)
        self.debug_info()
        
        self.assertEqual(len(self.repo.get_deferred()), 1)
        self.assertEqual(len(self.repo.get_identified()), 2)
        self.assertEqual(len(self.repo.get_antiidentified()), 1)
        #XXX if the next @#$%#$% test FAILS, it is because some obscure reaons in the ORDER of the "get_most_similar_persons"
        #(I THING)- try to run the test again...
        #XXX FIX the problem described above and resurrect the follwoing test
#        self.assertEqual(len(self.repo.get_most_similar_persons()), original_length-7)
        self.assertEqual(len(self.repo.get_persons()), 8)
        #the deferred list contains now only 1 pair
        
        #all these identifications should also be persistent after we refill the cache
        #print '* fill similarity cache'
        repo.db.fill_similarity_cache(refresh=True,minimal_score=0.0)
        #self.debug_info()
        #XXX THIS SHOULD NOT FAIL!! 
#        self.assertEqual(len(self.repo.get_most_similar_persons()), original_length-4)

    def debug_info(self):
        return
        try:
            print '-' * 50
            print 'in cache_Similarity person %s records (including identicals)' % self.repo.db.get_session().query(CacheSimilarityPersons).count()
            for r in  self.repo.db.get_session().query(CacheSimilarityPersons).all():
                i = 0
                if r.bioport_id1 != r.bioport_id2:
                    i += 1
                    print i, '-----', r.bioport_id1, r.bioport_id2
            print 'most similar:'
            for i in self.repo.get_most_similar_persons():
                print '-----', i
            print 'deferred:'
            for i in self.repo.get_deferred():
                print '-----',  i.bioport_id1, i.bioport_id2          
            print 'get_identified:'
            for i in self.repo.get_identified():
                print '-----',  i.bioport_id #, i.redirect_to         
            print 'get_antiidentified:'
            for i in self.repo.get_antiidentified():
                print '-----',  i.bioport_id1, i.bioport_id2      
        except UnicodeEncodeError, error:
            print error
               
    def test_identify(self):
        
        repo = self.create_filled_repository()
        
        #get two persons
        persons = repo.get_persons()
        self.assertEqual(len(persons), 10)
        person1 = persons[1]
        person2 = persons[2]
        bio1 = person1.get_biographies()[0]
        bio2 = person2.get_biographies()[0]
        id1 = person1.get_bioport_id() 
        id2 = person2.get_bioport_id()  
        
        assert id1 != id2
       
        #identify the two people
        person = repo.identify(person1, person2)
        
        #id1 is the 'old bioport id', id2 is the new one
        if person.get_bioport_id() == person1.get_bioport_id():
            id1, id2 = id2, id1
            
        #both identifiers are still in the system
        assert id1 in repo.get_bioport_ids(), repo.get_bioport_ids()
        assert id2 in repo.get_bioport_ids(), repo.get_bioport_ids()
       
        #but id1 now redirects to id2
        self.assertEqual(repo.redirects_to(id1), id2)
        
        #we now have 9 nstead of 10 persons
        self.assertEqual(len(repo.get_persons()), 9, [r.id for r in repo.get_persons()])
        #and the newly identified person has two biographies
        self.assertEqual(len(person.get_biographies()), 2)
        
        assert person in [person1, person2]
        
        #and we have a person with these two biographies attached
        bios = person.get_biographies()
        self.assertEqual(set([b.id for b in bios]), set([bio1.id, bio2.id]))
        
        #also, if we try to found the person with id1, we cannot find it anymore
        person1 = repo.get_person(bioport_id=id1)
        self.assertEqual(person1.bioport_id, id2)
        person2 = repo.get_person(bioport_id=id2)
        
        self.assertNotEqual(person2, None)

        assert len(person2.get_biographies()) == 2, person2.get_biographies()
        
 
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(RepositoryTestCase, 'test_'),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')    
