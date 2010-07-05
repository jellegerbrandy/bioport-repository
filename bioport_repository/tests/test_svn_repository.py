#import os
#import common_testcase
#from common_testcase import * 
#
#from svn_repository import *
#
#
#class Test_svn_repository(CommonTestCase):
#    
#        
#    def test_create_file(self):
#        self.repo.create_file('test_file', 'content_of_file')
#        f = self.repo.get_file('test_file')
#        self.assertEqual(f.read(), 'content_of_file')
#        
#        f = open(os.path.join(SVN_REPOSITORY_LOCAL_COPY, 'test_file'))
#        self.assertEqual(f.read(), 'content_of_file')
#        
#        self.repo.create_dir('xxx', 'content_of_file')
#        self.repo.create_file('xxx/test_file', 'content_of_file')
#        self.repo.commit('commit more test cases')
#        fn = os.path.join(SVN_REPOSITORY_LOCAL_COPY, 'test_file')
#        assert os.path.exists(fn)
#        f = self.repo.get_file('xxx/test_file')
#        self.assertEqual(f.read(), 'content_of_file')
#        
#        self.assertEqual(len(self.repo.ls('xxx')), 1, self.repo.ls('xxx'))
#        
#    def test_create_dir(self): 
#        repo = self.repo
#        
#        #at the initial stage, the repo is empty
#        ls = [fn for fn in os.listdir(SVN_REPOSITORY_LOCAL_COPY) if not fn.startswith('.')]
#        self.assertEqual(len(ls), 0,ls) 
#        repo.create_dir('test1', log_message='een test')
#        repo.create_dir('test2', log_message='een test')
#        repo.commit('commit testfiles')
#        #add a source
#        ls = repo.ls()
#        self.assertEqual(len(ls), 2, ls)
#        ls = [fn for fn in os.listdir(SVN_REPOSITORY_LOCAL_COPY) if not fn.startswith('.')]
#        self.assertEqual(len(ls), 2, ls)
#        ls = os.listdir(SVN_REPOSITORY_LOCAL_COPY)
#        repo.remove('test2')
#        repo.commit('removed 1 test file')
#        
#        ls = [fn for fn in os.listdir(SVN_REPOSITORY_LOCAL_COPY) if not fn.startswith('.')]
#        self.assertEqual(len(ls), 1, ls)
#        
#        ls = repo.ls()
#        self.assertEqual(len(ls), 1, ls)
#        
#        
#        repo.create_dir('test3', log_message='een test')
#        repo.create_file('test3/test_file', 'content_of_file')
#        
#        repo.remove('test3')
#        repo.commit('yeyeye')
#        ls = repo.ls()
#        self.assertEqual(len(ls), 1, ls)
#        repo.remove('test1')
#        repo.commit('yeyeye')
#        ls = repo.ls()
#        self.assertEqual(len(ls), 0, ls)
#        ls = os.listdir(SVN_REPOSITORY_LOCAL_COPY)
#        ls = [x for x in ls if not x.startswith('.')]
#        self.assertEqual(len(ls), 0, ls)
#        
#        
#if __name__ == "__main__":
#    unittest.main()
#    