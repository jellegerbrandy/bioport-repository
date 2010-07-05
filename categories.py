##! /usr/bin/python    
##encoding=utf-8

#rubrieken (van Els)
#
from db_definitions import Category 
def fill_table(session):    
    categories = """ 
       1. Adel en vorstenhuizen
       2. Bedrijfsleven (incl. bankwezen, industrie, handel, landbouw, techniek, transport)
       3. Beeldende kunsten & vormgeving (incl. architectuur)
       4. Kerk en godsdienst
       5. Koloniale en overzeese betrekkingen en handel
       6. Krijgsmacht
       7. Letterkunde (incl. dichtkunst, journalistiek)
       8. Maatschappelijke bewegingen (incl. protest, oproer, vakbeweging)
       9. Misdaad
      10. Onderwijs & wetenschappen
      11. Politiek (incl. diplomatie, landsbestuur)
      12. Radio en TV
      13. Rechtspraak
      14. Sport en vrije tijd
      15. Uitvoerende kunsten (muziek, toneel, dans, cabaret etc.)
      16. Zorg (incl. liefdadigheid, gezondheidszorg, sociale zorg)
      17. Overig
    """

    categories = """ 
       1. Adel en vorstenhuizen
       2. Bedrijfsleven
       3. Beeldende kunsten & vormgeving
       4. Kerk en godsdienst
       5. Koloniale en overzeese betrekkingen en handel
       6. Krijgsmacht en oorlog
       7. Letterkunde
       8. Maatschappelijke bewegingen
       9. Rechtspraak
      10. Onderwijs & wetenschappen
      11. Politiek en bestuur
      12. Radio en TV
      14. Sport en vrije tijd
      15. Uitvoerende kunsten
      16. Zorg
      17. Overig
    """

    ls = categories
    ls = ls.split('\n')
    ls = [l.strip().split('.', 1) for l in ls if l.strip()]
    ls = [(int(nr), s.strip()) for nr, s in ls] 
    #print ls
    #delete existing data
    session.query(Category).delete()
#        assert 0, 'The table %s already contains information -- please empty it first' % Category.__tablename__
    for nr, name in ls:
        session.add(Category(id=nr, name=name))
    session.commit()
    
