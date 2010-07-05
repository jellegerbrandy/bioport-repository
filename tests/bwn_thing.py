#from repository import Repository
#
#repo = Repository(
#              db_connection='mysql://root@localhost/bioport_play'
#               )
#               
#source = repo.get_source('bwn')
#bios = repo.get_biographies(source=source)
#for bio in bios:
#    print '"%s":"%s",' % ('/'.join(bio.get_value('url_biografie').split('/')[-2:])[3:], bio.id)
##        