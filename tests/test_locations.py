from common_testcase import CommonTestCase, unittest 
from BioPortRepository.db import *

class DBRepositoryTestCase(CommonTestCase):

        
    def test_workflow(self): 
        db = self.db
        db._update_geolocations_table(limit=100)
        locations = db.get_locations()
        self.assertEqual(len(locations), 100)
            
        #get the locations that start with 'a'
        locations = db.get_locations(startswith='a')
        assert locations
        #there is one Anjum (within the first 100 on the list) 
        locations = db.get_locations(name='Anjum')
        print [l.full_name for l in locations]
        self.assertEqual(len(locations), 1)
        
       
        location = locations[0]
        
        location.adm1 = '02' #amsterdam is in friesland
        
        #set the location of a biography
        
        #get a biography
        self.create_filled_repository()
        biography = self.db.get_biographies()[0]
        
        biography.add_or_update_event(type="birth", place_id=location.ufi)
if __name__ == "__main__":
    unittest.main()
