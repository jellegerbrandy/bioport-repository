from bioport_repository.tests.common_testcase import CommonTestCase, unittest 

class IdentifierTestCase(CommonTestCase):
        
    def test_generators(self):
        
        i = self.repo 
        
        id1 = i.db.fresh_identifier()
        id2 = i.db.fresh_identifier()
        self.assertNotEqual(id1, id2)
        
        self.create_filled_repository()
        some_person = self.repo.get_persons()[4]
        id = some_person.get_bioport_id()
        self.repo.delete_person(some_person)
        
        
        
if __name__ == "__main__":
    unittest.main()