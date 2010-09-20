import os
import pickle

from common import CommonTestCase, unittest
from bioport_repository.similarity.similarity import Similarity
from bioport_repository.person import Person
from bioport_repository.biography import Biography
from bioport_repository.source import Source


class SimilarityTestCase(CommonTestCase):

    def setUp(self):
        CommonTestCase.setUp(self)
        self.source = source = Source(id='bioport_test')
        self.repo.save_source(source)        
        self.sim = Similarity()
        self.similarity_score = self.sim.similarity_score
        
    def _add_person(self, naam, 
        geboortedatum=None,
        sterfdatum=None,
        ):
        #make a new biography
        bio = Biography( id = 'bioport_test/test_bio_%s' % naam, source_id=self.source.id)
        
        bio.from_args( 
              url_biografie='http://ladida/didum', 
              naam_publisher='nogeensiets', 
              url_publisher='http://pbulihser_url',
              naam=naam,
              geboortedatum=geboortedatum,
              sterfdatum=sterfdatum,
              )
        
        #save it
        self.repo.add_biography(bio)
        return bio.get_person()
    
    def test_similarity(self):
        p1 = self._add_person('Jan', geboortedatum='1000', sterfdatum='2000')
        p2 = self._add_person('Jan', geboortedatum='1000', sterfdatum='2000')
        p3 = self._add_person('Piet Jan')
        p4 = self._add_person('Piet', geboortedatum='1000', sterfdatum='2000')
        self.assertEqual(self.similarity_score(p1, p2), 1)
        assert  0 < self.similarity_score(p1, p3)< 1
        assert self.similarity_score(p1, p4) < 1.0
        return
        #get some persons
        p1 = Person('1', repository=self.repo)
        self.repo.save_person(p1)
        p1.add_biography(Biography().from_args(
           geboortedatum='1900-01-01', sterfdatum='1910-02-02', 
           naam='Jan Klaassen', 
           naam_publisher='xxx',
           url_biografie='http://www.inghist.nl',
           url_publisher='http://www.inghist.nl',
           ) )
        
    def _read_testsets(self): 
        fn_identified =  os.path.join(os.path.dirname(__file__), 'data', 'identified_examples.pickle')
        self._identified = []
        for bio1, bio2 in pickle.load(open(fn_identified)):
            self._identified.append((bio1, bio2))
    def _add_bio(self,bio, id):
        bio = Biography( id='bioport_test/%s' % id, source_id=self.source.id).from_string(bio)
        bio.set_value('bioport_id', '')
        self.repo.add_biography(bio)
        return bio.get_person()
    
    def xtest_examples(self):
        self._read_testsets()
        ls= []
        i = 0
        for bio1, bio2 in self._identified:
            i += 1
            p1 = self._add_bio(bio1, id=str(i*2))
            p2 = self._add_bio(bio2, id=str(i*2 + 1))
            score = self.similarity_score(p1, p2)
            print i, score, p1, p2 
            ls.append((score, p1, p2))
        ls.sort()
        print 'LOWEST SCORE'
        for score, p1, p2 in ls[:5]:
            print score, 
            print p1, 
            print p2 
    
    def test_cases_to_optimize(self):
        #0.82241156589 <Person Maria Elisabeth Ghijben with id 64720037> <Person Ghyben-maay, Elizabeth with id 05140558>
        p1 = self._add_person(naam ="Maria Elisabeth Ghijben")
        p2 = self._add_person(naam="Ghyben-maay, Elizabeth")
        score = self.similarity_score(p1, p2)
        print score, p1, p2

    def test_new_thing(self):
        persons = self.repo.get_persons()
        sim = Similarity(persons[1], persons)
        sim.compute()
        sim.sort()

    def test_most_similar_persons(self):
        repo= self.repo
        self.assertEqual(len(self.repo.get_persons()) ,10)
        self.repo.db.fill_similarity_cache(minimal_score=0.0)
        for r in self.repo.db.get_session().query(CacheSimilarityPersons).all():
            assert r.bioport_id1 <= r.bioport_id2, (r.bioport_id1, r.bioport_id2)

        ls = repo.get_most_similar_persons(size=3)
        ls = list(ls)
        self.assertEqual(len(ls) ,3)
        score, p1, p2  = ls[0]
        self.assertNotEqual(p1.get_bioport_id(), p2.get_bioport_id())

        ls = repo.get_most_similar_persons(bioport_id=p1.bioport_id)
        for score, pa, pb in ls:
            assert p1.bioport_id in [pa.bioport_id, pb.bioport_id]
        ls = repo.get_most_similar_persons(source_id=self.repo.get_sources()[0].id)
        ls = repo.get_most_similar_persons(search_name='jan')


def test_suite():
    test_suite = unittest.TestSuite()
    tests = [SimilarityTestCase]
    for test in tests:
        test_suite.addTest(unittest.makeSuite(test))
    return test_suite

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')

