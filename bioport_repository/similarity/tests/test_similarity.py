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
#0.9 <Person Catharina Mulder with id 64689327> <Person Mulder, Catharina with id 35032709>
#0.923561076605 <Person Mina Kruseman with id 35194114> <Person Kruseman, Wilhelmina Jacoba Pauline Rudolphine with id 24639010>
#0.941023017903 <Person Heenvliet, Elizabeth van with id 42821187> <Person Liesbeth van Heenvliet with id 48994382>
#0.951326933936 <Person Nispen van Sevenaer, Johannes Antonius Christianus Arnoldus van with id 72595512> <Person Jan van Nispen van Sevenaer with id 98377030>
#.
# 0.731287 Albertus Lomeyer        Lomeier (Lomeyer, Lomarus) Albertus
if __name__ == "__main__":
    unittest.main() #defaultTest='SimilarityTestCase.test_cases_to_optimize')
