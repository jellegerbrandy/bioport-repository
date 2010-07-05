from names.similarity import Similarity
from names.common import to_ymd
class Similarity(Similarity):
    def __init__(self, person=None, persons=None):
        self._computed =False
        self._person = person
        self._persons = persons
    
    def compute(self):
        """compute the similarity scores between self._person and each element of self._persons
        
        save the score as an attribute on each Person in self._persons
        returns self._persons"""
        if self._computed:
            return self._persons
        for person in self._persons:
            person.score = self.similarity_score(self._person, person)
        self._computed = True
        return self._persons

    def _decennium(self, s):
        """ """
        if s:
            ymd= to_ymd(s)  
            y, m, d = ymd
            return y
    def similarity_score(self, p1, p2):
        """compute how similar these two persons are"""
        #people with the same birth dates gat a high score
        b1 = self._decennium(p1.geboortedatum())
        b2 = self._decennium(p2.geboortedatum())
        d1 = self._decennium(p1.sterfdatum())
        d2 = self._decennium(p2.sterfdatum())
        
#        if p1.geboortedatum() and p1.geboortedatum() == p2.geboortedatum()  and p1.sterfdatum() and p1.sterfdatum() == p2.sterfdatum():
#            return 1.0
            
        max_ratio_names = 0
        #compare the names
        for n1 in p1.get_names():
            for n2 in p2.get_names():
                max_ratio_names = max(self.ratio(n1, n2, optimize=True), max_ratio_names)
        ratio = max_ratio_names
        #XXX better not use "deceninium" here, but the difference between the years
        #(say, penalize for more than 10 years difference)
        if b1 and b2:
            if  b1 == b2:
                ratio = (ratio + 2.0 ) /3.0
            elif abs(b1-b2) < 3:
                ratio = (ratio + 1.0 ) /2.0
            else:
                ratio = (ratio + 0.8) / 2.0
        
        if d1 and d2:
            if d1 == d2:
                ratio = (ratio + 2.0 ) /3.0
            elif abs(d1-d2) < 3:
                ratio = (ratio + 1.0 ) /2.0
            else:
                ratio = (ratio + 0.8) / 2.0
                
        if not d1 and not d2:
            ratio = (ratio + 0.98) / 2.0
        return ratio
                
    def sort(self):
        self.compute()
        ls = [(p.score, p) for p in self._persons]
        ls.sort(reverse=True)
        self._persons = [p[1] for p in ls]
        return self._persons