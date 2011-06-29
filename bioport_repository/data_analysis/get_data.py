import urllib
URL = "http://biografischportaal.nl/personen/json"
URL = "http://localhost:8094/bioport/personen/json"

STEP = 500
def get_data():
    for i in range(0, 80*1000, STEP):
        url = '%s?start=%s&size=%s' % (URL, i, STEP)
        fn =  'data/personen_%s-%s.json' % (i, i + STEP)
        print 'retrieving %s' % url
        urllib.urlretrieve(url, fn)


def make_one_big_dict():
    d = {}
    for i in range(0, 80*1000, STEP):
#        if i > 1000:
#            break
        fn =  'data/personen_%s-%s.json' % (i, i + STEP)
        print 'opening', fn
        s= open(fn).read()
        s = s.replace('null', 'None')
        s = s.replace('false', 'False')
        s = s.replace('["', '[u"')
        s = s.replace(', "', ', u"')
        ls = eval(s)
        for person in ls:
            d[person['bioport_id']] = person
    
    return d

#print 'getting data'
#get_data()  
print 'done'
print 'make_one_big_dict '
d = make_one_big_dict()
print 'saving..'
fn_out = 'persons_all.py'
open(fn_out, 'w').write(unicode(d))
print 'done'