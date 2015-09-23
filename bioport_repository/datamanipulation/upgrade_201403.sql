# stap 1: ontdubbelen van person_source records
alter ignore table `bioport`.`person_source`
  drop column `id`,
  add primary key (`bioport_id`,`source_id`)
;

#
create table `person_source2` (
  `bioport_id` varchar(50) default null,
  `source_id` varchar(20) default null,
#  primary key (`bioport_id`,`source_id`),
  key `ix_person_source_bioport_id` (`bioport_id`),
  key `ix_person_source_source_id` (`source_id`)
) engine=myisam auto_increment=3681233 default charset=latin1;

create table person_source2 like person_source;
insert `person_source2` select * from `person_source` group by bioport_id, source_id;
alter table person_source2 drop column id, add primary key(bioport_id,source_id);

alter table


drop trigger if exists trigger_birthday;
create trigger trigger_birthday after update on person
  begin
    #set birthday;
    # set initial;
    #set invisible;

  end;
