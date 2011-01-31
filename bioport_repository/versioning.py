

class Version:
    """represents a version of a BioDes document"""
    def __init__(self, 
        biography,
        ):
        """
       
        arguments:
            biography : an instance of biography
        
        """
        self.biography = biography
        r = biography.record
        self.user = r.user
        self.time = r.time
        self.comment = r.comment
        self.document_id =  r.id
        self.version = r.version
    
    def __str__(self):
        return '<Version %s of  %s by %s of %s (%s)>' % (self.version, self.document_id, self.user, self.time, self.comment )
    def __repr__(self):
        return self.__str__()