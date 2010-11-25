#!/usr/bin/env python
"""
ALTER TABLE `bioport`.`antiidentical` ADD INDEX `bioport_id1`(`bioport_id1`);
ALTER TABLE `bioport`.`defer_identification` ADD INDEX `bioport_id1`(`bioport_id1`);

"""
"""
ALTER TABLE `bioport`.`person_soundex` ADD COLUMN `is_from_family_name` boolean  AFTER `soundex`;
ALTER TABLE `bioport`.`person_name` ADD COLUMN `is_from_family_name` boolean  ;
"""
"""
2009114:
Excute the following querys:

ALTER TABLE `person` MODIFY COLUMN `search_source` TEXT  CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
 ADD COLUMN `remarks` TEXT  AFTER `search_source`;

 ALTER TABLE `person` ADD COLUMN `status` INT  AFTER `search_source`;




"""
#
#from bioport_repository.repository import *
#
#DSN = 'mysql://root@localhost/bioport_play'
#repo = Repository(db_connection=DSN) 
#
#def upgrade_persons(repo):
#    for person in repo.get_persons():
#        print person
#        if 'bioport' in [s.id for s in person.get_sources()]:
#            print 'SET'
#            person.status = 2
#            repo.save_person(person)
#
#def set_everything_without_a_status_to_niet_bewerkt(): 
#    sql = """update person  set person.status = 12  where person.status is null"""        
#    repo.get_session.execute(sql) 
#    
