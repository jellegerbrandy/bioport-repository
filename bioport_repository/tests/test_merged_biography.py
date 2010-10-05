from bioport_repository.tests.common_testcase import CommonTestCase, unittest 
from bioport_repository.merged_biography import MergedBiography
from lxml import etree


class TestMergedBiography(CommonTestCase):
        
    def test_biography(self):
        self.create_filled_repository()
        repo = self.repo
        #get an existing biography
        bios = repo.get_biographies()[1:4]
        merged = MergedBiography(bios)
        bios = merged.get_biographies()
        ls = []
        for bio in bios:
            ls += bio.get_names() 
        assert ls
        self.assertEqual(len(merged.get_names()),len( ls ))
        self.assertEqual(set([n.to_string() for n in merged.get_names()]), set([n.to_string() for n in ls])) 
        
        #check if the default value works
        self.assertEqual(len(merged.get_illustrations(default=['123'])), 1)
        
        for bio in bios:
            bio.set_value('geboortedatum', '')
            self.assertEqual(bio.get_value('geboortedatum'), None)
        self.assertEqual(merged.get_value('geboortedatum'), None)
        #if dates are consistent with each other, they "add up"
        bios[-1].set_value('geboortedatum', '2000')
        self.assertEqual(merged.get_value('geboortedatum'), '2000')
        bios[-2].set_value('geboortedatum', '2000-02')
        self.assertEqual(merged.get_value('geboortedatum'), '2000-02')
        bios[-3].set_value('geboortedatum', '2000-02-01')
        self.assertEqual(merged.get_value('geboortedatum'), '2000-02-01')
        self.assertEqual(merged.geboortedatum(), '2000-02-01')
        bios[-3].add_or_update_event(type='birth', when='', date_text='ongeveer') #, notBefore=notBefore, notAfter=notAfter, place=place)
        
        self.assertEqual(merged.geboortedatum(), 'ongeveer', etree.tostring(merged.get_event('birth')))
        
        #test if all relevaent information ends up in the "merged biodes" file
        bios[-3].set_value('geboortedatum', '2000-02-01')
        
        doc = merged.to_xml()
        self.assertEqual(doc.get_value('geboortedatum'), '2000-02-01', doc.to_string())
        self.assertEqual(doc.get_value('birth_date'), '2000-02-01')


 
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestMergedBiography),
        ))


if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')    


