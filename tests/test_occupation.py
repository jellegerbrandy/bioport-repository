from common_testcase import CommonTestCase, unittest 
from BioPortRepository.db import *

class OccupationTestCase(CommonTestCase):

        
    def test_workflow(self): 
        db = self.db
        repo = self.repo
        db._update_occupations_table()
        occupations= repo.get_occupations()
        self.assertEqual(len(occupations), 38)
        some_occupation = occupations[4]
        id = some_occupation.id
        assert repo.get_occupation(id)
        
        #get a biography
        self.create_filled_repository()
        biography = self.db.get_biographies()[0]
        biography.add_or_update_state(type='occupation', idno=str(some_occupation.id), text=some_occupation.name)
        
        #assert 0, biography.to_string()
        
        
        #now, if we get the occupation from the biography, it is the one we just set
        assert biography.get_states(type='occupation')
        #self.assertEqual(biography.get_state(type='occupation').get('idno'), id)
if __name__ == "__main__":
    unittest.main()
