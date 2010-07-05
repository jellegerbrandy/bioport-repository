#this is the singleton implementation of wikipedia (http://en.wikipedia.org/wiki/Singleton_pattern#Python)
class Singleton(type):
    def __init__(self, name, bases, dict):
        super(Singleton, self).__init__(name, bases, dict)
        self.instance = None
 
    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kw)
 
        return self.instance
    
#USAGE: 
#class MyClass(object):
#    __metaclass__ = Singleton
# 
#print MyClass()
#print MyClass()

#class SortOfSingleton(type):
#    def __init__(self, name, bases, dict):
#        super(Singleton, self).__init__(name, bases, dict)
#        self.instance = {}
# 
#    def __call__(self, *args, **kw):
#        if self.instance is None:
#            self.instance = super(Singleton, self).__call__(*args, **kw)
# 
#        return self.instance

class BioPortException(Exception):
    pass

def is_valid_bioport_id(s):
    return s.isdigit()
