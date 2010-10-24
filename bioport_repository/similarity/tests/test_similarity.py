import os
import pickle

from common import CommonTestCase, unittest
from bioport_repository.similarity.similarity import Similarity

class SimilarityTestCase(CommonTestCase):
    
    def setUp(self):
        CommonTestCase.setUp(self)
        self.sim = Similarity()
        self.similarity_score = self.sim.similarity_score
    
    def assert_similarity_order(self, ls):
        def _format_person(p):
            return '%s (%s-%s)' % (p.get_names(), p.get_value('birth_date'), p.get_value('death_date'))
        sims = [(self.similarity_score(p1, p2), p1, p2) for p1, p2 in ls]
        for i, score in enumerate(sims):
            if i > 1:
                self.assertTrue(sims[i-1][0] >= sims[i][0], 'Expected %s, %s [%s] to be more similar than %s and %s [%s]' % (
                            _format_person(sims[i-1][1]), _format_person(sims[i-1][2]), sims[i-1][0],
                            _format_person(sims[i][1]), _format_person(sims[i][2]), sims[i][0]
                            ))
            
    def test_similarity(self):
        p1 = self._add_person('Jan', geboortedatum='1000', sterfdatum='2000')
        p2 = self._add_person('Jan', geboortedatum='1000', sterfdatum='2000')
        p3 = self._add_person('Piet Jan')
        p4 = self._add_person('Piet', geboortedatum='1000', sterfdatum='2000')
        p5 = self._add_person('Jan', geboortedatum='1001', sterfdatum='2000')
        self.assertEqual(self.similarity_score(p1, p2), 1)
        self.assertTrue(0 < self.similarity_score(p1, p3)< 1)
        self.assertTrue(self.similarity_score(p1, p4) < 1.0)
        self.assertTrue(self.similarity_score(p1, p5) < 1.0)
    
    def test_similarity_with_dates(self):
        p1 = self._add_person('Lucky', geboortedatum='1000', sterfdatum='2000')
        p2 = self._add_person('Lucky', geboortedatum='', sterfdatum='2000')
        p3 = self._add_person('Lucky', geboortedatum='1000', sterfdatum='')
        p4 = self._add_person('Lucky', geboortedatum='', sterfdatum='')
        self.assert_similarity_order([
          (p1, p1),
          (p1, p2),
          (p1, p3),
          (p1, p4),
        ]) 
        p2 = self._add_person('Lucky', geboortedatum='1001', sterfdatum='2000')
        p3 = self._add_person('Lucky', geboortedatum='1900', sterfdatum='2000')
       
        self.assert_similarity_order([
          (p1, p1),
          (p1, p2),
          (p1, p3),
        ]) 
        
        p1 = self._add_person('Lucky, Pozzo Vladimir Estragon', geboortedatum='1000', sterfdatum='2000')
        p2 = self._add_person('Luckie, Pozzo Vladimir Estragon', geboortedatum='1000', sterfdatum='2000')
        p3 = self._add_person('Lucky, Pozzo Vladimir Estragon', geboortedatum='', sterfdatum='')
        p4 = self._add_person('Luckie, Pozzo Vladimir Estragon', geboortedatum='', sterfdatum='')
        score1 = Similarity.similarity_score(p1, p2) 
        score2 = Similarity.ratio(p1.get_names()[0], p2.get_names()[0])
        #given the fact that they have the same birth and death dates, the scores of p1 and p2 shoudl imporve wrt the "bare" names
        self.assertTrue(score1 > score2)
        self.assert_similarity_order([
          (p1, p1),
          (p1, p2),
          (p1, p3),
          (p1, p4),
        ])
        
    def test_surely_equal(self):
        p0 = self._add_person('Estragon', geboortedatum='1000', sterfdatum='2000')
        p1 = self._add_person('Estragon', geboortedatum='1000', sterfdatum='2000')
        p2 = self._add_person('Estragon', geboortedatum='1001', sterfdatum='2000')
        p3 = self._add_person('Estragon', geboortedatum='1000-12-12', sterfdatum='2000')
        p4 = self._add_person('Estragon', geboortedatum='1000', sterfdatum='2001')
        p5 = self._add_person('Vladimir', geboortedatum='1000', sterfdatum='2000')
        p6 = self._add_person('Estragon', geboortedatum='1000', sterfdatum='')
        p7 = self._add_person('Mercier Camier', geboortedatum='1000', sterfdatum='1200')
        p8 = self._add_person('Camier, Mercier', geboortedatum='1000', sterfdatum='1200')
        p9 = self._add_person('Dongen, Kees van', geboortedatum='1000', sterfdatum='1200')
        p10 = self._add_person('Kees van Dongen', geboortedatum='1000', sterfdatum='1200')
        p11 = self._add_person(names=['Kees van Dongen', 'Cornelius van Dongen'], geboortedatum='1000', sterfdatum='1200')
        p12 = self._add_person('Mercier', geboortedatum='1000', sterfdatum='1200')
        bio = self._create_biography(name='Dongen, Kees van')
        p12.add_biography(bio)
        self.repo.save_biography(bio)
        self.assertTrue(Similarity.are_surely_equal( p0, p1))
        self.assertFalse(Similarity.are_surely_equal(p0, p2))
        self.assertTrue(Similarity.are_surely_equal(p0, p3))
        self.assertFalse(Similarity.are_surely_equal(p0, p4))
        self.assertFalse(Similarity.are_surely_equal(p0, p5))
        self.assertFalse(Similarity.are_surely_equal(p0, p6))
        self.assertTrue(Similarity.are_surely_equal(p7, p8))
        self.assertTrue(Similarity.are_surely_equal(p9, p10))
        self.assertTrue(Similarity.are_surely_equal(p9, p11))
        self.assertTrue(Similarity.are_surely_equal(p9, p12))
        self.assertTrue(Similarity.are_surely_equal(p10, p12))
       
    def _read_testsets(self): 
        fn_identified =  os.path.join(os.path.dirname(__file__), 'data', 'identified_examples.pickle')
        self._identified = []
        for bio1, bio2 in pickle.load(open(fn_identified)):
            self._identified.append((bio1, bio2))
            
if __name__ == "__main__":
    unittest.main() #defaultTest='SimilarityTestCase.test_cases_to_optimize')
