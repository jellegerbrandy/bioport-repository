import os

from bioport_repository.tests.common_testcase import CommonTestCase, unittest 
from common_testcase import SQLDUMP_FILENAME

class SearchTestCase(CommonTestCase):
    
    def test_get_persons(self):
        #XXX remove this
        #os.remove(SQLDUMP_FILENAME)
        self.create_filled_repository()
        repo = self.repo
       
        #check sanity
        self.assertEqual(len(repo.get_persons()), 10)
       
        #add a number of persons
        pius = self._add_person('Pius IX')
        #we do not want to find Pius IX if we search for 'ik'
        self.assertEqual(repo.get_persons(search_name='IX'), [pius])
        assert pius not in repo.get_persons(search_name='ik')
        
        self.assertEqual(len(repo.get_persons(search_soundex=u'molloyx')), 1)
        self.assertEqual(len(repo.get_persons(search_soundex=u'boschma')), 9, self.repo.get_persons())
        self.assertEqual(len(repo.get_persons(search_soundex=u'bosma')), 9) #, self.repo.get_persons())
        self.assertEqual(len(repo.get_persons(search_soundex='bo?ma')), 9)
        self.assertEqual(len(repo.get_persons(search_name=u'"mollo??"')), 1)
        self.assertEqual(len(repo.get_persons(search_name=u'"mollo*"')), 1)

        
        return
        
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(SearchTestCase, 'test'),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')

