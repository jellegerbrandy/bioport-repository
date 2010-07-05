import os
from common_testcase import CommonTestCase, this_dir, unittest
from BioPortRepository.repository import Source
from BioPortRepository.db_definitions import STATUS_NEW
class RepositoryTestCase(CommonTestCase):
    def test_download_changed_bios(self):
        print 'DONWNLOADING knaw/list.xml'
        repo = self.repo
        url = os.path.abspath(os.path.join(this_dir, 'data/knaw/list.xml'))
        #add some sources source
        SOURCE_ID = u'test1'
        BASE = 10
        src = Source(id=SOURCE_ID, url=url , description='knaw test dinges')
        repo.add_source(src)
        repo.download_biographies(src)
        self.assertEqual(len(repo.get_persons()), BASE + 5)
        
        old_persons = [repo.get_person(bioport_id) for bioport_id in repo.get_bioport_ids()]
        #download again
        print 'DOWNLOADING knaw/list.xml a SECOND TIME'
        repo.download_biographies(src)
        #nothing should have changed
        self.assertEqual(len(repo.get_persons()),BASE +  5)
        self.assertEqual(set([p.bioport_id for p in old_persons]), set([p.bioport_id for p in repo.get_persons()]))
        
        #now we change the biographies that are available in some of the sources
        url2 = os.path.abspath(os.path.join(this_dir, 'data/knaw_changed/list.xml'))
        src.url = url2
        repo.download_biographies(src)
#        ls = [p.title() for p in  old_persons]
#        ls.sort()
#        print 'original bios', ls
#        ls = [p.title() for p in  repo.get_persons()]
#        ls.sort()
#        print 'new bios', ls
        #the new url has one biograrphy less, and one new one. 
        #we remove the one that has disappeared, so the number of persons should now be 6
#        self.assertEqual(len(repo.get_persons()),BASE + 6,)
        #all of the old bioport_ids should still be available
        for p in old_persons:
            assert p.bioport_id in repo.get_bioport_ids()
        
        #3 has disappleared
        #4 has changed name
        #5 has changed location, but should have the same data
        #7 is a new entry
        persons = {}
        for person in repo.get_persons(source_id=SOURCE_ID):
            knaw_bio = None
            for bio in person.get_biographies():
                if bio.get_source().id == SOURCE_ID:
                    knaw_bio = bio
            person.knaw_bio = knaw_bio 
            id = knaw_bio.get_id().split('/')[1]
            for i in range(1,6):
                if id == '00%s' % i:
                    persons[i] = person
            if id == '107':
                persons[107] = person
        #person 3 has disappeared - but what does that mean?
        #person[3]
        #person 4 has a changed name
        #XXX we should test this somehow
        assert 'changed' in persons[4].name().volledige_naam(), persons[4].name().volledige_naam()
        #person 5 has changed location
        assert persons[5].knaw_bio.source_url.endswith('005a.xml'), persons[5].knaw_bio.source_url
        #person 7 is a new entry
        self.assertEqual( persons[5].status, STATUS_NEW) 
        
    def test_delete_effects(self):
        repo = self.repo
        url = os.path.abspath(os.path.join(this_dir, 'data/knaw/list.xml'))
        SOURCE_ID = u'test1'
        src_knaw = src = Source(id=SOURCE_ID, url=url , description='knaw test dinges...')
        self.assertEqual(src.url, url)
        repo.add_source(src)
        repo.download_biographies(src)
        repo.delete_biographies(src)
        src_knaw.url = os.path.join(this_dir, 'data/knaw2/list.xml')
        repo.download_biographies(src_knaw)
        
        i= 0
        for person in repo.get_persons():
            i += 1
            bio = repo.get_bioport_biography(person)
            bio.set_value('geboortedatum_tekst',  '000%s'% i)       
            
    def test_identification_and_editing_effects(self):
        repo = self.repo
        #we start with 10 people
        BASE = 10
        SOURCE_ID = u'test1'
        SOURCE_ID2 = u'test2'
        self.assertEqual(len(repo.get_persons()), BASE)
        url = os.path.abspath(os.path.join(this_dir, 'data/knaw/list.xml'))
        src_knaw = src = Source(id=SOURCE_ID, url=url , description='knaw test dinges...')
        self.assertEqual(src.url, url)
        repo.add_source(src)
        repo.download_biographies(src)
#        print url
#        print src.url
        persons = repo.get_persons()
        self.assertEqual(len(persons), BASE+5)
       
        url = os.path.abspath(os.path.join(this_dir, 'data/knaw2/list.xml'))
        src = Source(id=SOURCE_ID2, url=url , description='knaw test dinges')
        repo.add_source(src)
        repo.download_biographies(src)
        persons = repo.get_persons()
        
        #check sanity
        self.assertEqual(len(persons), BASE + 10)
        i = 0
        for person in repo.get_persons():
            i += 1
            bio = repo.get_bioport_biography(person)
            bio.set_value('geboortedatum_tekst',  '000%s'% i)
            repo.save_biography(bio)            

        persons = {} 
        j = 0
        for person in repo.get_persons():
            j += 1
            knaw_bio = None
            for bio in person.get_biographies():
                if bio.get_source().id in [SOURCE_ID, SOURCE_ID2]:
                    knaw_bio = bio
                    person.knaw_bio = knaw_bio 
                    id = knaw_bio.get_id().split('/')[1]
#                    print j, id
                    for i in range(1,11):
                        if id == '00%s' % i:
                            persons[i] = person       
       
        #person 3 will diasppear, person 5 will change location
        person1 = repo.identify(persons[3], persons[7])
        person2 = repo.identify(persons[5], persons[8])
        #check sanity
        self.assertEqual(len(person1.get_biographies()), 4)
        self.assertEqual(len(person2.get_biographies()), 4)
        #we identified to pairs, so now we have two persons less
        self.assertEqual(len(repo.get_persons()), BASE+ 8)
        
        i = 0
        for person in repo.get_persons():
            i += 1
            bio = repo.get_bioport_biography(person)
            bio.set_value('geboortedatum_tekst',  '000%s'% i)
            repo.save_biography(bio)        
#        print [p.get_biographies()[-1].get_local_id() for p in  repo.get_persons()]
        src_knaw.url = os.path.join(this_dir, 'data/knaw_changed/list.xml')
        repo.download_biographies(src_knaw)
#        print [p.get_biographies()[-1].get_local_id() for p in  repo.get_persons()]
        self.assertEqual(len(repo.get_persons()), BASE + 8)
        
        #get the person gaain
        person1 = repo.get_person(person1.bioport_id)
        person2 = repo.get_person(person2.bioport_id)
        #TODO: THIS SHOULD BE 3 when we strt merging bioport biographies
        self.assertEqual(len(person2.get_biographies()), 4)
        
        i= 0
        for person in repo.get_persons():
            i += 1
            bio = repo.get_bioport_biography(person)
            bio.set_value('geboortedatum_tekst',  '000%s'% i)
            
    def test_removal_of_bios(self):
        #one of the biographies of person1 has been removed
        #XXX but what is the desired effct here?
        #1. the biography should not be there anymore
        #2. the bioport_id shoudl still exist
        #3. if we have no more biographies for this person, the person shoudl disappear 
        repo = self.repo
        url1 = os.path.abspath(os.path.join(this_dir, 'data/knaw/list.xml'))
        url2 = os.path.abspath(os.path.join(this_dir, 'data/knaw2/list.xml'))
        
        src = Source(id=u'test', url=url1 , description='knaw test dinges')
        repo.add_source(src)
        
        repo.download_biographies(src)
        
        person3 = repo.get_biography(local_id='test/003').get_person()
        bioport_id3 = person3.bioport_id
       
        #download again
        #now we change the biographies that are available in some of the sources
        src.url = url2
        repo.delete_biographies(src)
        repo.download_biographies(src)
        
        #now the biography of person3 does not exist anymore
        self.assertEqual(len(repo.get_biographies(local_id='test/003')), 0)
        #and neither does person3 himself
        repo.delete_orphaned_persons()
        assert person3.bioport_id not in [p.bioport_id for p in repo.get_persons()],  [(p.bioport_id, p.get_biographies()) for p in repo.get_persons()]
        
        #now we re-download the old data
        src.url = url1
        repo.delete_biographies(src)
        repo.download_biographies(src)
        #and we have the 5 old biographies again
        self.assertEqual(len(repo.get_persons(source_id=src.id)), 5)
        self.assertEqual(len(repo.get_biographies(local_id='test/003')), 1)
        #it is very import that our newly re-donloaed test/003 has the same bioport id as before
        self.assertEqual(repo.get_biography(local_id='test/003').get_person().bioport_id, bioport_id3)
       
        #now, we do the same exercise of removing and re-adding, but this time we identify test/003 with test/002
        person2 = repo.get_biography(local_id='test/002').get_person()
        new_person = repo.identify(person2, person3)
        self.assertEqual(len(repo.get_persons(source_id=src.id)), 4)
        self.assertEqual(len(new_person.get_biographies()), 2)
        src.url = url2
        repo.delete_biographies(src)
        repo.download_biographies(src)
        self.assertEqual(len(repo.get_biographies(source_id=src.id)), 5)
        self.assertEqual(len(repo.get_persons(source_id=src.id)), 5, [p.get_biographies() for p in repo.get_persons(source_id=src.id)])
        new_person = repo.get_person(bioport_id=new_person.bioport_id)
#        self.assertEqual(len(new_person.get_biographies()), 1, new_person.get_biographies())
        
if __name__ == "__main__":
    unittest.main(defaultTest='RepositoryTestCase.test_removal_of_bios')        
    
