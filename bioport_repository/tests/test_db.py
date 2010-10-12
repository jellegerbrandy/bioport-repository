from bioport_repository.tests.common_testcase import CommonTestCase, unittest 
from bioport_repository.db import Source, BiographyRecord, NaamRecord, PersonRecord, SoundexRecord, SourceRecord, Biography, RelBioPortIdBiographyRecord
from bioport_repository.db_definitions import RelPersonCategory


class DBRepositoryTestCase(CommonTestCase):
        
    def test_basics(self): 
        db = self.db
        
        assert 'biography' in db.engine.table_names()
        assert 'naam' in db.engine.table_names()
        assert 'soundex' in db.engine.table_names(), db.engine.table_names()

    def test_manipulate_source(self):
        src = Source(id='123')
        self.db.add_source(src)
        self.assertEqual(len(self.db.get_session().query(SourceRecord).all()), 3)
        self.assertEqual(len(self.db.get_sources()), 3)
        self.db.delete_source(src)
        self.assertEqual(len(self.db.get_sources()), 2)
    
    def test_manipulate_biographies(self): 
        """tests for adding and deleting biographies"""
        n_base = len(self.db.get_biographies())
        n_base_naam = self.db.get_session().query(NaamRecord).count()
        n_base_soundex = self.db.get_session().query(SoundexRecord).count()
        self.assertEqual(len(self.db.get_session().query(BiographyRecord).all()), n_base )
        src = Source(id='123')
        self.repo.save_source(src)
        
        bio1 = Biography(id='ladida', source_id=src.id)
        bio1.from_args(naam_publisher="1", url_biografie="http://www.url.com/1", url_publisher="http:///url2.com", naam="jantje")
        
        self.db.add_biography(bio1)
    
        #we have added one new biography, with one name that corresponds to one single soundex
        self.assertEqual(len(self.db.get_biographies()), n_base + 1)
        self.assertEqual(len(self.db.get_session().query(BiographyRecord).all()), n_base + 1)
        self.assertEqual(len(self.db.get_session().query(NaamRecord).all()), n_base_naam + 1)
        self.assertEqual(len(self.db.get_session().query(SoundexRecord).all()), n_base_soundex + 1)
        
        #this biography has one oauthor
        bio1.set_value('auteur', ['Johan'])
        self.db.save_biography(bio1)
        self.assertEqual(len(bio1.get_value('auteur', [])), 1, bio1.to_string())
        
        bio2 = Biography(id='ladida2', source_id=src.id)
        bio2.from_args(naam_publisher="1", url_biografie="http://www.url.com/1", url_publisher="http:///url2.com", naam="jantje")
        self.db.add_biography(bio2)
        self.assertEqual(len(self.db.get_biographies()), n_base + 2)
    
    def test_update_biographies(self):
        #set up a source
        src = Source(id='123')
        self.repo.save_source(src)
        bio1 = Biography(id='id1', source_id=src.id)
        bio1.from_args(naam_publisher="1", url_biografie="http://www.url.com/1", url_publisher="http:///url1.com", naam="name1", text='text1')
        self.db.add_biography(bio1)
        bio1.from_args(naam_publisher="1", url_biografie="http://www.url.com/1", url_publisher="http:///url1.com", naam="name1", text='text2')
        self.db.add_biography(bio1)
        person = self.db.get_person(bio1.get_bioport_id())
        self.assertEqual(person.snippet(), 'text2')
        
    def test_source_updating(self):
        self.create_filled_repository()    
        src = self.repo.get_source(id=u'knaw')
        self.db.delete_biographies(src)
        self.assertEqual(len(self.db.get_biographies(source=src)), 0)
        
        self.repo.download_biographies(src)
        self.assertEqual(len(self.db.get_biographies(source=src)), 5) 
        
    def test_update_persons(self):
        self.create_filled_repository(sources=1)
        self.repo.db.update_persons()
        
    def test_saving_of_categories(self): 
        repo = self.repo
        #get some person from the database
        
        p = repo.get_persons()[1]
        #set some properties here and there
        categories = [1,2,3]
        bio = p.get_bioport_biography()
        bio.set_category(categories)
        
        #save the changes in the repository
        self.repo.save_biography(bio)
        
        #sanity checks: see if the person knows about this
        self.assertEqual(len(bio.get_states(type='category')), len(categories))
        self.assertEqual(len(p.get_bioport_biography().get_states(type='category')), len(categories))
        self.assertEqual(len(p.get_merged_biography().get_states(type='category')), len(categories))
        

        #do we have these categories in the database
        self.assertEqual(repo.db.get_session().query(RelPersonCategory).filter(RelPersonCategory.bioport_id==p.get_bioport_id()).count(), len(categories))
        #now try to find the person again, and see if the changes hold (and are in the db)
        
        new_p = repo.get_person(p.get_bioport_id())
        self.assertEqual(len(new_p.get_merged_biography().get_states(type='category')), len(categories))
        self.assertTrue(p in repo.get_persons(category=categories[0]))
        
    def test_get_persons(self):
        self.create_filled_repository()
        repo = self.repo
       
        #check sanity
        self.assertEqual(len(repo.get_persons()), 10)
       
        #identify  two persons so we have more interesting queries
        repo.identify(repo.get_persons(source_id=u'knaw')[0], repo.get_persons(source_id=u'knaw2')[-1])
        
        self.assertEqual(len(repo.get_persons()), 9)
        
        self.assertEqual(len(repo.get_persons(source_id=u'knaw2')), 5)
        self.assertEqual(len(repo.get_persons(source_id2=u'knaw2')), 5)
        self.assertEqual(len(repo.get_persons(source_id=u'knaw', source_id2=u'knaw2')), 1)
        self.assertEqual(len(repo.get_persons(is_identified=True)), 1)
        
        self.assertEqual(len(repo.get_persons(category=1)), 1)
        
        self.assertEqual(len(repo.get_persons(search_name='jan')), 1)
        self.assertEqual(len(repo.get_persons(search_term='molloy')), 1)
        self.assertEqual(len(repo.get_persons(has_illustrations=True)), 2)
        self.assertEqual(len(repo.get_persons(has_illustrations=False)), 7)
        
        self.assertEqual(len(repo.get_persons(geboortejaar_min='1778')), 7)
        self.assertEqual(len(repo.get_persons(geboortejaar_max='1777')), 2)
        self.assertEqual(len(repo.get_persons(geboortejaar_min='1778', geboortejaar_max='1778')), 1)

        self.assertEqual(len(repo.get_persons(sterfjaar_min='1858')), 7)
        self.assertEqual(len(repo.get_persons(sterfjaar_max='1857')), 2)
        self.assertEqual(len(repo.get_persons(sterfjaar_min='1858', sterfjaar_max='1858')), 1)
        self.assertEqual(len(repo.get_persons(search_name=u'molloyx')), 1)
        self.assertEqual(len(repo.get_persons(search_name=u'"molloyx"')), 1)
        
        self.assertEqual(len(repo.get_persons(geboorteplaats='Amsterdam')), 3)
        self.assertEqual(len(repo.get_persons(geboorteplaats='Am*')), 3)
        self.assertEqual(len(repo.get_persons(sterfplaats='*en')), 3)

        self.assertEqual(len(repo.get_persons(sterfplaats='Lisse')), 1)
        
        self.assertEqual(len(repo.get_persons(search_soundex=u'molloyx')), 1)
        self.assertEqual(len(repo.get_persons(search_soundex=u'boschma')), 9, self.repo.get_persons())
        self.assertEqual(len(repo.get_persons(search_soundex=u'bosma')), 9) #, self.repo.get_persons())
        self.assertEqual(len(repo.get_persons(search_soundex='bo?ma')), 9)
        self.assertEqual(len(repo.get_persons(search_name=u'"mollo??"')), 1)
        self.assertEqual(len(repo.get_persons(search_name=u'"mollo*"')), 1)

    def test_complex_geboorte_date_get_persons_full(self):
        self.create_filled_repository()
        repo = self.repo
        qry = dict(geboortejaar_min=1888, geboortemaand_min=6, geboortedag_min=1)
        qry.update(dict(geboortejaar_max=1893, geboortemaand_max=3, geboortedag_max=1))
        self.assertEqual(len(repo.get_persons(**qry)), 1)
        del(qry['geboortedag_min'], qry['geboortedag_max'])
        self.assertEqual(len(repo.get_persons(**qry)), 1)
        
    def test_complex_levend_date_get_persons_full(self):
        self.create_filled_repository()
        repo = self.repo
        qry = dict(levendjaar_min=1778, levendmaand_min=1, levenddag_min=12)
        qry.update(dict(levendjaar_max=1778, levendmaand_max=2, levenddag_max=21))
        self.assertEqual(len(repo.get_persons(**qry)), 2)
        qry.update(dict(levendjaar_min=1770, levendjaar_max=1770))
        self.assertEqual(len(repo.get_persons(**qry)), 1)
        
    def test_complex_geboorte_date_get_persons_partial(self):
        self.create_filled_repository()
        repo = self.repo
        qry = dict(geboortemaand_min="1", geboortedag_min="1")
        qry.update(dict(geboortemaand_max="2", geboortedag_max="1"))
        self.assertEqual(len(repo.get_persons(**qry)), 3)
        qry.update(dict(geboortemaand_max="1", geboortedag_max="10"))
        self.assertEqual(len(repo.get_persons(**qry)), 2)
    def test_complex_sterf_date_get_persons_full(self):
        self.create_filled_repository()
        repo = self.repo
        qry = dict(sterfjaar_min=1904, sterfmaand_min=6, sterfdag_min="1")
        qry.update(dict(sterfjaar_max=1965, sterfmaand_max="5", sterfdag_max="20"))
        self.assertEqual(len(repo.get_persons(**qry)), 2)
        qry['sterfmaand_max'] = '11'
        self.assertEqual(len(repo.get_persons(**qry)), 3)
    def test_complex_sterf_date_get_persons_partial(self):
        self.create_filled_repository()
        repo = self.repo
        qry = dict(sterfmaand_min="1", sterfdag_min="10")
        qry.update(dict(sterfmaand_max="2", sterfdag_max="20"))
        self.assertEqual(len(repo.get_persons(**qry)), 2)
        qry['sterfdag_max'] = '25'
        self.assertEqual(len(repo.get_persons(**qry)), 3)

    def test_trans_year_boundary_sterf_date_get_persons(self):
        self.create_filled_repository()
        repo = self.repo
        qry = dict(sterfmaand_min="11", sterfdag_min="20")
        qry.update(dict(sterfmaand_max="1", sterfdag_max="20"))
        self.assertEqual(len(repo.get_persons(**qry)), 2)
        qry['sterfdag_max'] = '31'
        self.assertEqual(len(repo.get_persons(**qry)), 3)
        #Let's check that a date with the year only is not returned
        self.db.get_session().execute(
            "UPDATE person set sterfdatum='1882'"
            " WHERE sterfdatum='1882-01-15'")
        self.assertEqual(len(repo.get_persons(**qry)), 2)

    def test_hide_invisible(self):
        self.create_filled_repository()
        repo = self.repo
        person = repo.get_persons()[1]
        person.status = 5 
        repo.save_person(person)
        self.assertEqual(len(repo.get_persons(hide_invisible=True)), 9)
        self.assertEqual(len(repo.get_persons(hide_invisible=False)), 10)

    def test_get_all_places(self):
        self.create_filled_repository()
        db = self.db
        all_places = db.get_places()
        expected_all_places = [u"'s Gravenhage", u'Ameide', u'Amsterdam', u'Brussel, Belgi\xeb', u'De Bilt', u'Down, Groot Brittani\xeb', u'Driebergen', u'Gent, Belgi\xeb', u'IJsbrechtum', u'Leiden', u'Lisse', u'Newham, Groot Brittani\xeb', u'Paesens, Frankrijk', u'Tilburg']
        self.assertEqual(all_places, expected_all_places)
        sterf_places = db.get_places('sterf')
        expected_sterf_places = [u"'s Gravenhage", u'Amsterdam', u'De Bilt', u'Driebergen', u'Gent, Belgi\xeb', u'Leiden', u'Lisse', u'Newham, Groot Brittani\xeb']
        self.assertEqual(sterf_places, expected_sterf_places)
        geboorte_places = self.repo.get_places('geboorte')
        expected_geboorte_places = [u'Ameide', u'Amsterdam', u'Brussel, Belgi\xeb', u'Down, Groot Brittani\xeb', u'Gent, Belgi\xeb', u'IJsbrechtum', u'Paesens, Frankrijk', u'Tilburg']
        self.assertEqual(geboorte_places, expected_geboorte_places)

    def test_delete_biographies(self): 
        """check if we clean up after ourselves when deleting biographies"""
        session = self.repo.db.get_session()
        
        #just check some general sanity
        #we have 10 biographies in two sources, 5 bios each
        self.assertEqual(session.query(BiographyRecord).count(), 10)
        
        self.assertEqual(len(self.repo.get_sources()), 2)
        source1, source2 = self.repo.get_sources()
        self.assertEqual(len(self.repo.get_persons()), 10)
        self.assertEqual(len(self.repo.get_persons(source_id=source1.id)), 5)
        self.assertEqual(len(self.repo.get_persons(source_id=source2.id)), 5)
       
        #we identify two persons from source1 and source2
        self.repo.identify(
           self.repo.get_persons(source_id=source1.id)[0],
           self.repo.get_persons(source_id=source2.id)[0],
           )
        #and we now have 9 persons, but still 5 from each
        self.assertEqual(len(self.repo.get_persons()), 9)
        self.assertEqual(len(self.repo.get_persons(source_id=source1.id)), 5)
        self.assertEqual(len(self.repo.get_persons(source_id=source2.id)), 5)
        
        #we delete the biographies for one source
        self.repo.delete_biographies(source1)
            
        #the sources are still there
        self.assertEqual(len(self.repo.get_sources()), 2)
        #and also the bioport_ids we used
        self.assertEqual(len(self.repo.get_bioport_ids()), 10)
        
        #but the biographies are now only 5 
        self.assertEqual(len(self.repo.get_biographies()), 5)
        self.assertEqual(session.query(BiographyRecord).count(), 5)
        #there are also only 5 persons left
        self.assertEqual(session.query(PersonRecord).count(), 5)
        self.assertEqual(len(self.repo.get_persons()), 5)
        
        #and we should have no persons associated with source1 anymore
        self.assertEqual(self.repo.get_persons(source_id=source1.id), [])
        
        #however, we still should remember with which bioport_ids our biogrpahies were associated
        self.assertEqual(session.query(RelBioPortIdBiographyRecord).count(), 10)
        
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(DBRepositoryTestCase, 'test_'),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
