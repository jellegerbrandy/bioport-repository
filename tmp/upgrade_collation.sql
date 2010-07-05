alter table biography modify id varchar(50) charset utf8 collate utf8_bin;

alter table relbioportidbiography modify biography_id varchar(50) charset utf8 collate utf8_bin;

alter table relbiographyauthor modify biography_id varchar(50) charset utf8 collate utf8_bin;

update relbioportidbiography set biography_id='dvn/Baerle' where biography_id='dvn/baerle'; 
update biography set id='dvn/Baerle' where id='dvn/baerle'; 
#update relbioportidbiography set biography_id='dvn/Toppen' where biography_id='dvn/Toppen'; 

update relbioportidbiography set biography_id='dvn/Dijk2' where biography_id='dvn/dijk'; 
update biography set id='dvn/Dijk2' where id='dvn/dijk'; 
update relbioportidbiography set biography_id='dvn/dijk' where biography_id='dvn/Dijk'; 
update biography set id='dvn/dijk' where id='dvn/Dijk'; 
update relbioportidbiography set biography_id='dvn/Dijk' where biography_id='dvn/Dijk2'; 
update biography set id='dvn/Dijk' where id='dvn/Dijk2'; 

update relbioportidbiography set biography_id='dvn/MariavanNassau2' where biography_id='dvn/MariavanNassau'; 
update biography set id='dvn/MariavanNassau2' where id='dvn/MariavanNassau'; 

update relbioportidbiography set biography_id='dvn/MariavanNassau' where biography_id='dvn/mariavannassau'; 
update biography set id='dvn/MariavanNassau' where id='dvn/mariavannassau'; 

update relbioportidbiography set biography_id='dvn/mariavanNassau' where biography_id='dvn/MariavanNassau2'; 
update biography set id='dvn/mariavannassau' where id='dvn/MariavanNassau2'; 
#maria%20van%20nassau
#toppen
#dijk
