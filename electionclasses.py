


class ElectionGroup(object):

    def __init__(self,description,year):
        self.description = description
        self.year = year
    pass



class Kommune(object):

    def __init__(self,kommunenavn,kommunekode):
        self.kommunenavn = kommunenavn
        self.kommunekode = kommunekode
    pass



class Candidate(object):

    def __init__(self,name,party)
    self.name = name
    self.party = party
    pass



class Party(object):
    
    def __init__(self,partinavn,partinummer,partikode,partitype):
        self.partinavn = partinavn
        self.partinummer = partinummer
        self.partikode = partikode
        self.partitype = partitype

        
    #Partinavn
    #Partinummer (4-sifre unik identifikator av partiet)
    #Partikode (unik partikode for partiet)
    #Type parti (stortingsparti, landsdekkende parti, lokalt parti)
    #Godkjenning (må være på plass for at et parti skal kunne stille liste i et valg)
    #Forenklet behandling (har betydning for hvor mange underskrifter som trengs for å godkjenne en liste)
    pass



class Election(object):
    #En valgtype, f.eks kommunevalg, bydelsutvalg, fylkestingsvalg, stortingsvalg, sametingsvalg. 
    #Områdenivå for valget (kommune eller fylke)
    #"Single area"-flagg (vanlige valg er "single area", sametingsvalg er det ikke)
    #Renummerering, strykning, tilføyelse (writein)
    #Aldersgrense
    #Flagg for om kandidater må ha stemmerett
    #Diverse regler for valgoppgjør (blant annet "first divisor in Sainte-Lague")
    #Flagg som angir hvem som utfører endelig telling (brukes i Sametingsvalget)

    def __init__(self,valgtype,year):
        self.first_divisor = 1.4
        self.age_limit = 18
        self.valgtype = valgtype
        self.year = year
    pass


class Contest(object):
    #Delvalg, eks. et kommunevalg
    #Knyttet til tellinger (via "contest report")
    #Knyttet til valgoppgjør (settlement)
    #Kan overskrive en del instillinger på valg, f.eks aldersgrense
    #Maks antall kandidater, stemmegivninger, etc
    #Flagg som angir hvem som utfører endelig telling (kan overstyre verdien satt på valgnivå)
    #Knyttet til stemmeseddel/partiliste

    def __init__(self,area, number_of_seats):
        self.number_of_seats = number_of_seats
        self.area = area


    def perform_settlement(self):
        self.settlement = Settlement(self)

    pass


class ElectionConfiguration(object):
    pass


class PollingPlace(object):
    pass


class PartyList(object):
    pass


class CountResult(object):
    pass


class Settlement(object):

    def __init__(self, contest):
        self.contest = contest
        self.status = 'Not started'
    #Valgoppgjør
    pass

class CandidateSeat(object):
    #mandat
     def __init__(self, settlement,seatwinner):
         self.settlement = settlement
         self.seatwinner = seatwinner
    
    pass
