from bioport_repository.tests.common_testcase import CommonTestCase, unittest 
from bioport_repository.db import *


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
        
        self.assertEqual(len(self.db.get_session().query(BiographyRecord).all()), n_base + 1)
        self.assertEqual(len(self.db.get_session().query(NaamRecord).all()), n_base_naam + 1)
        self.assertEqual(len(self.db.get_session().query(SoundexRecord).all()), n_base_soundex + 1)
        
        #this biography has one oauthor
        bio1.set_value('auteur', ['Johan'])
        self.db.save_biography(bio1)
        self.assertEqual(len(bio1.get_value('auteur', [])), 1, bio1.to_string())
        
        self.assertEqual(len(self.db.get_biographies()), n_base + 1)
        bio2 = Biography(id='ladida2', source_id=src.id)
        bio2.from_args(naam_publisher="1", url_biografie="http://www.url.com/1", url_publisher="http:///url2.com", naam="jantje")
        self.db.add_biography(bio2)
        self.assertEqual(len(self.db.get_biographies()), n_base + 2)
        self.db.delete_biography(bio1)
        self.assertEqual(len(self.db.get_biographies()), n_base + 1)
  
    def test_source_updating(self):
        self.create_filled_repository()    
        src = self.repo.get_source(id='knaw')
        self.db.delete_biographies(src)
        self.assertEqual(len(self.db.get_biographies(source=src)), 0)
        
        self.repo.download_biographies(src)
        self.assertEqual(len(self.db.get_biographies(source=src)), 5) 
#    def xxx_test_get_authors(self):
#        """temporarily disabled becuase not used"""
#        self.create_filled_repository()
#        repo = self.repo
#        
#        self.assertEqual(len(repo.get_authors()), 7)
#        
#        bio = repo.get_biographies()[2]
#        self.assertEqual(len(bio.get_value('auteur')), 1)
#        
#        self.assertEqual(len(repo.get_authors(biography=bio)), 1)
#        
#        self.assertEqual(len(repo.get_authors(beginletter='v')), 2)
#        self.assertEqual(len(repo.get_authors(search_term='ronger')), 1)
              

        
        
#
#    def xxx_test_get_author(self):
#        self.create_filled_repository()
#        repo = self.repo
#       
#        some_author = repo.get_authors()[3]
#        self.assertEqual(repo.get_author(some_author.id).name, some_author.name)
#        self.assertEqual(len(repo.get_authors(search_term='ronger')), 1)
        
    def test_update_persons(self):
        self.create_filled_repository(sources=1)
        self.repo.db.update_persons()
        
        
    def test_get_persons(self):
        self.create_filled_repository()
        repo = self.repo
       
#        assert 0, list(repo.db.get_session().execute('select * from person'))
        self.assertEqual(len(repo.get_persons()), 10)

        
#        some_author = repo.get_authors()[0]
#        self.assertEqual(len(repo.get_persons(auteur_id=some_author.id)), 1)
        
        self.assertEqual(len(repo.get_persons(source_id=u'knaw2')), 5)
#        self.assertEqual(len(repo.get_persons(auteur_id=some_author.id, source_id='knaw')), 1)
        self.assertEqual(len(repo.get_persons(is_identified=True)), 0)
#        assert 0, [[s.attrib for s in p.get_merged_biography().get_states(type='category')] for p in repo.get_persons()]
#        assert 0,[r.category_id for r in repo.db.get_session().query(RelPersonCategory).all()]

        self.assertEqual(len(repo.get_persons(category=1)), 1)
        self.assertEqual(len(repo.get_persons(search_name='jan')), 1)
        self.assertEqual(len(repo.get_persons(search_term='molloy')), 1)
        self.assertEqual(len(repo.get_persons(has_illustrations=True)), 2)
        self.assertEqual(len(repo.get_persons(has_illustrations=False)), 8)
        
        self.assertEqual(len(repo.get_persons(geboortejaar_min='1778')), 8)
        self.assertEqual(len(repo.get_persons(geboortejaar_max='1777')), 2)
        self.assertEqual(len(repo.get_persons(geboortejaar_min='1778', geboortejaar_max='1778')), 1)

        self.assertEqual(len(repo.get_persons(sterfjaar_min='1858')), 7)
        self.assertEqual(len(repo.get_persons(sterfjaar_max='1857')), 3)
        self.assertEqual(len(repo.get_persons(sterfjaar_min='1858', sterfjaar_max='1858')), 1)
        self.assertEqual(len(repo.get_persons(search_name=u'molloyx')), 1)
        self.assertEqual(len(repo.get_persons(search_name=u'"molloyx"')), 1)
        
        self.assertEqual(len(repo.get_persons(geboorteplaats='Amsterdam')), 3)
        self.assertEqual(len(repo.get_persons(geboorteplaats='Am*')), 4)
        self.assertEqual(len(repo.get_persons(sterfplaats='*en')), 3)

        self.assertEqual(len(repo.get_persons(sterfplaats='Lisse')), 1)
        
        self.assertEqual(len(repo.get_persons(search_soundex=u'molloyx')), 1)
        self.assertEqual(len(repo.get_persons(search_soundex='bosma')), 9)
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


if __name__ == "__main__":
    unittest.main()
