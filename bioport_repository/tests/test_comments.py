from datetime import datetime

from bioport_repository.tests.common_testcase import CommonTestCase, unittest 
from bioport_repository.person import Person


class CommentTestCase(CommonTestCase):

    def test_comment_creation_and_listing(self):
        p1 = Person('1234', repository=self.repo)
        comments = p1.get_comments()
        self.assertEqual(comments.count(), 0)
        comment_text = "This bio is really accurate!"
        p1.add_comment(text=comment_text)
        comments = p1.get_comments()
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments[0].text, comment_text)
        self.assertEqual(comments[0].created.toordinal(), datetime.now().toordinal())
        self.assertEqual(comments[0].submitter, 'Anonymous')
        p1.add_comment(text=comment_text + ' is not true!')


def test_suite():
    test_suite = unittest.TestSuite()
    tests = [CommentTestCase]
    for test in tests:
        test_suite.addTest(unittest.makeSuite(test))
    return test_suite 

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
