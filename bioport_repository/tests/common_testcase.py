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
from bioport_repository.tests.config import SQLDB, DSN

from gerbrandyutils import sh


THIS_DIR = os.path.split(os.path.abspath(__file__))[0]
SVN_REPOSITORY  = os.path.abspath(os.path.join(THIS_DIR, 'data/bioport_repository'))
SVN_REPOSITORY_LOCAL_COPY = os.path.abspath(os.path.join(THIS_DIR, 'data/bioport_repository_local_copy'))
IMAGES_CACHE_LOCAL = os.path.join(THIS_DIR, 'tmp')
SQLDUMP_FILENAME = os.path.join(THIS_DIR, 'data/bioport_mysqldump.sql')


class CommonTestCase(unittest.TestCase):
    
    _fill_repository = True

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
              db_connection=DSN,
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
        
        # remove also all data from the database
        self.repo.db.metadata.drop_all()
        shutil.rmtree(IMAGES_CACHE_LOCAL)
        #self.repo.db.namenindex.db.metadata.drop_all()
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
        self.repo.db.get_session().flush()
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
        
        def parse_dsn(s):
            return sqlalchemy.engine.url._parse_rfc1738_args(s)

        dsn = parse_dsn(DSN)
        username = dsn.username or ""
        passwd = dsn.password or ""
        if not passwd:
            sh('mysqldump -u %s bioport_test > %s' % (username, SQLDUMP_FILENAME))
        else:
            sh('mysqldump -u %s -p%s bioport_test > %s' % (username, passwd, SQLDUMP_FILENAME))
        self._is_filled = True
        return self.repo


class CommonTestCaseTest(CommonTestCase):
    
    def test_sanity(self):
        self.assertEqual(len(self.repo.get_sources()), 2)
        self.assertEqual(len(self.repo.get_biographies()), 10)
        self.assertEqual(len(self.repo.get_persons()), 10)

def create_mysqldump():      
    """create a .sql file that is used for setting up the database for each test"""
    open(SQLDUMP_FILENAME,'w').write('show tables')
    unittest.main(defaultTest='CommonTestCase.create_filled_repository_from_scratch')   


