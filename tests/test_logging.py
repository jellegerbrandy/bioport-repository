from common_testcase import CommonTestCase, unittest , this_dir
from BioPortRepository.db import *
class LoggingTestCase(CommonTestCase):

    
    def log_message_exists(self, msg, user, table, id):
        session= self.repo.get_session()
        if type(id) == type(0):
            record_id_int = id
        else:
            record_id_str = id
        qry = session.query(ChangeLog).filter(
              ChangeLog.msg==msg,  
              ChangeLog.user==user, 
              ChangeLog.table==table, 
              ChangeLog.record_id_int==record_id_int, 
              ChangeLog.record_id_str==record_id_str,
              )
        qry = qry.order_by(ChangeLog.timestamp)
        rs = qry.all()
        assert rs
        return rs[-1]
   
    def last_log_message(self):
        session= self.repo.db.get_session()
        qry = session.query(ChangeLog)
        qry = qry.order_by(ChangeLog.timestamp)
        return qry.all()[-1]
    
    def print_last_log_message(self): 
        r = self.last_log_message()
        return '%s-%s-%s-%s: %s' % (r.timestamp, r.user, r.table, r.record_id_str or r.record_id_int, r.msg)
        
    def test_logging(self):
        repo = self.repo
        
        url = 'file://%s' % os.path.abspath(os.path.join(this_dir, 'data/knaw/list.xml'))
        source = Source(id=u'test1', url=url , description='test')
        self.repo.add_source(source)
        self.assertEqual(self.last_log_message().table, 'source')
        self.repo.download_biographies(source)
        self.assertTrue(self.last_log_message().msg.startswith('saved biography'))
        self.assertEqual(self.last_log_message().table, 'biography')
        #download biographies
        
        #change a biography
        
        person = repo.get_persons()[3]
        repo.save_person(person)
        self.assertEqual(self.last_log_message().table, 'person')
        
        repo.add_biography(person.get_bioport_biography())
        self.assertEqual(self.last_log_message().table, 'biography')
        
    def test_get_log(self):
        self.create_filled_repository()
        self.repo.get_log_messages()
if __name__ == "__main__":
    unittest.main()
