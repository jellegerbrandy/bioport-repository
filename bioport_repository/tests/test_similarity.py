
#XXX move this test to similarity/tests
from bioport_repository.tests.common_testcase import CommonTestCase, unittest
from bioport_repository.db_definitions import CacheSimilarityPersons
from bioport_repository.similarity.similarity import Similarity


class SimilarityTestCase(CommonTestCase):
    def test_new_thing(self):
        persons = self.repo.get_persons()
        sim = Similarity(persons[1], persons)
        sim.compute()
        sim.sort()
#        for p in sim._persons:
#            print unicode(p), p.score
        
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


