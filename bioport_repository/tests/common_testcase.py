import os
import sys
import unittest
import shutil
import atexit
import subprocess

from plone.memoize import instance
import sqlalchemy

from bioport_repository.repository import Repository
from bioport_repository.source import Source


THIS_DIR = os.path.split(os.path.abspath(__file__))[0]
SVN_REPOSITORY  = os.path.abspath(os.path.join(THIS_DIR, 'data/bioport_repository'))
SVN_REPOSITORY_LOCAL_COPY = os.path.abspath(os.path.join(THIS_DIR, 'data/bioport_repository_local_copy'))
IMAGES_CACHE_LOCAL = os.path.join(THIS_DIR, 'tmp')
SQLDUMP_FILENAME =os.path.join(THIS_DIR, 'data/bioport_mysqldump.sql')


KNOWN_GOOD_DSNS = (
    'mysql://localhost/bioport_testx',
    'mysql://user:pass@localhost/bioport_test',
    'mysql://localhost/bioport_test',
    )
    

def sh(cmd):
    """Run a shell command and wait for completion.
    Raises an exception if something goes bad.
    """
    return subprocess.check_call(cmd, shell=True)
    

class CommonTestCase(unittest.TestCase):
    
    _fill_repository =True
   
    def known_good_dsn(self):
        """try to find a good connection string for the DB"""
        for dsn in KNOWN_GOOD_DSNS:
            engine = sqlalchemy.create_engine(dsn)
            try:
                engine.connect()
                return dsn 
            except sqlalchemy.exc.DBAPIError:
                pass
        #if we arrive here we cannot find a good DSN
        raise Exception('Could not find a good DSN. This is the list we tried:\n\t' + '\n\t'.join(KNOWN_GOOD_DSNS)) 
    @instance.clearafter
    def setUp(self):               
        if os.path.isdir(SVN_REPOSITORY):
            shutil.rmtree(SVN_REPOSITORY)
        sh('svnadmin create %s --pre-1.4-compatible' % SVN_REPOSITORY)
        if not os.path.isdir(IMAGES_CACHE_LOCAL):
            os.mkdir(IMAGES_CACHE_LOCAL)

        self.repo = Repository(
              svn_repository_local_copy = SVN_REPOSITORY_LOCAL_COPY, 
              svn_repository='file://%s' % SVN_REPOSITORY,
              db_connection=self.known_good_dsn(),
              images_cache_local=IMAGES_CACHE_LOCAL,
              )
              
        self.repo.db.metadata.drop_all()
        if self._fill_repository:
            if not os.path.isfile(SQLDUMP_FILENAME):
                self.create_filled_repository_from_scratch()
            self.create_filled_repository()
        else:
            self.repo.db.metadata.create_all()

        self.db = self.repo.db
        
    def tearDown(self):
        #clean out the repository
        #get whatever data there was
        sh('rm -rf %s' % SVN_REPOSITORY ) 
        sh('rm -rf %s' % SVN_REPOSITORY_LOCAL_COPY ) 
        
        #remove also all data from the database
        self.repo.db.metadata.drop_all()
        shutil.rmtree(IMAGES_CACHE_LOCAL)
#        self.repo.db.namenindex.db.metadata.drop_all()
        return
   
    def create_filled_repository(self, sources=None):
        """create  a repository filled with example data"""
        if not self._fill_repository:
            return self.repo
        sql_string = open(SQLDUMP_FILENAME).read().decode('latin1')
        import bioport_repository.tests
        testdir = os.path.dirname(bioport_repository.tests.__file__)
        datadir = os.path.join(testdir, 'data')
        sql_string = sql_string.replace('{{{test_data_dir}}}', testdir)
        self.repo.db.get_session().execute(sql_string)
        self.repo.db.get_session().commit()
        self._fill_repository = False #dont fill the repository again
        return self.repo
    
    def create_filled_repository_from_scratch(self, sources=2):
        #create a repo filled with some data

        self.repo.db.metadata.create_all()
        url = 'file://%s' % os.path.abspath(os.path.join(THIS_DIR, 'data/knaw/list.xml'))
        source = Source(id=u'knaw', url=url , description='test')
        self.repo.add_source(source)
        self.repo.download_biographies(source)
        url = 'file://%s' % os.path.abspath(os.path.join(THIS_DIR, 'data/knaw2/list.xml'))
        if sources > 1:
            source = Source(id=u'knaw2', url=url , description='test')
            self.repo.add_source(source)
            self.repo.download_biographies(source)
        self.repo.db._update_category_table()
        sh('mysqldump bioport_test > %s' % SQLDUMP_FILENAME)
        self._is_filled =True
        return self.repo
    
class CommonTestCaseTest(CommonTestCase):
    
    def test_sanity(self):
#        self.create_filled_repository()
        self.assertEqual(len(self.repo.get_sources()), 2)
        
        self.assertEqual(len(self.repo.get_biographies()), 10)
        self.assertEqual(len(self.repo.get_persons()), 10)

def create_mysqldump():      
    """create a .sql file that is used for setting up the database for each test"""
    open(SQLDUMP_FILENAME,'w').write('show tables')
    unittest.main(defaultTest='CommonTestCase.create_filled_repository_from_scratch')
    

def cleanup():
    try:
        os.remove(SQLDUMP_FILENAME)
    except OSError:
        pass        


# remove any sqldump test file which might have been left behind 
# by previous test runs, plus schedule its removal when the process
# exits
cleanup()
atexit.register(cleanup)


if __name__ == "__main__":
    create_mysqldump()
    unittest.main()
