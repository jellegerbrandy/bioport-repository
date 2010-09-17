from bioport_repository.tests.common_testcase import CommonTestCase, unittest 
from bioport_repository.person import Person

class PersonTestCase(CommonTestCase):
        
    def test_person_init(self):
        p1 = Person('1234', repository=self.repo)
        p2 = Person('2345')
        self.assertNotEqual(p1.id, p2.id)
        
        p1.remarks = u'ladida'
        self.repo.save_person(p1)
        p1.get_sources()
        p = self.repo.get_person(p1.get_bioport_id())
        assert p, [p.get_bioport_id() for p in self.repo.get_persons()]
        self.assertEqual(p.remarks, 'ladida' )
        
    def test_get_names(self):
        self.create_filled_repository(sources=1)
        p1 = self.repo.get_persons()[1]
        p2 = self.repo.get_persons()[2]
        names1 = p1.get_names()
        names2 = p2.get_names()
        n1 = len(names1)
        n2 = len(names2)
        assert names1 != names2, names1 + names2
        p = self.repo.identify(p1, p2)
        bio = self.repo.get_bioport_biography(p)
        self.assertEqual(len(p.get_names()), n1 + n2)
#        bio.set_value(names=['Malone'])
#        self.assertEqual(len(p.get_names()), 1, p.get_names())
        
    def test_search_source(self):
        self.create_filled_repository(sources=1)
        p1 = self.repo.get_persons()[1]
    
    def test_memoization(self):
        p1 = self.repo.get_persons()[1]
        p1.get_merged_biography()
        p1.get_merged_biography()
        p1.get_merged_biography()
        p1.get_merged_biography()

        
def test_suite():
    test_suite = unittest.TestSuite()
    tests = [PersonTestCase]
    for test in tests:
        test_suite.addTest(unittest.makeSuite(test))
    return test_suite

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')    



