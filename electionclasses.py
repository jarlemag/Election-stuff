
import settlement
import json
import unittest
import hashlib
import sys
import math

test_dict = json.load(open('test_data.json'))
data_dict = json.load(open('data.json'))

votetotals_drammen = data_dict["Drammen"]["voteTotals"].copy()
test_result = settlement.distribute_seats_wrapper(data_dict,"Drammen",silent = True)





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

    def __init__(self,name,party):
        self.name = name
        self.party = party
    pass



class Party(object):
    
    def __init__(self,partinavn,partinummer,partikode,partitype):
        self.partinavn = partinavn #Partinavn
        self.partinummer = partinummer #Partinummer (4-sifre unik identifikator av partiet)
        self.partikode = partikode #Partikode (unik partikode for partiet)
        self.partitype = partitype #Type parti (stortingsparti, landsdekkende parti, lokalt parti)

    
    #Godkjenning (må være på plass for at et parti skal kunne stille liste i et valg)
    #Forenklet behandling (har betydning for hvor mange underskrifter som trengs for å godkjenne en liste)

    pass



class Election(object):
     
    #Områdenivå for valget (kommune eller fylke)
    #"Single area"-flagg (vanlige valg er "single area", sametingsvalg er det ikke)
    #Renummerering, strykning, tilføyelse (writein)
    
    #Flagg for om kandidater må ha stemmerett
    #Flagg som angir hvem som utfører endelig telling (brukes i Sametingsvalget)

    def __init__(self,valgtype,year):
        self.first_divisor = 1.4
        self.age_limit = 18 #Aldersgrense
        self.valgtype = valgtype #En valgtype, f.eks kommunevalg, bydelsutvalg, fylkestingsvalg, stortingsvalg, sametingsvalg.
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


    def __init__(self,area, number_of_seats,election = Election('Ukjent',math.nan)):
        self.number_of_seats = number_of_seats
        self.area = area
        self.description = "Unknown"
        self.votetotals = {}
        self.contestreports = []
        self.validcontestreport = None
        self.election = election
        self.age_limit = self.election.age_limit


    def perform_settlement(self,verbose = False):
        self.settlement = Settlement(self,self.validcontestreport)
        self.result = self.settlement.distributeseats()

    pass


class ElectionConfiguration(object):
    pass


class PollingPlace(object):
    pass


class PartyList(object):
    pass


class ContestReport(object):
    #Tilsvarer valgprotokoll del B til D
    def __init__(self):
        self.votetotals = {}
    
    pass



class ContestFinalReport(object):
    #Tilsvarer den fullstendige valgprotokollen
    def __init__(self):
        self.votetotals = {}
    
    pass

class VoteCount(object):

    def __init__(self):
        pass
    pass



class BallotCount(object):
    def __init__(self):
        pass
    pass



class Settlement(object):

    def __init__(self,contest,contestreport,verbose = False,silent = False):
        self.contest = contest
        self.status = 'Not started'
        self.votetotals = contestreport.votetotals
        self.number_of_seats = contest.number_of_seats
        self.awardedseats_total = 0
        self.awardedseats = []
        self.currentseatwinner = ''
        self.verbose = verbose
        self.silent = silent
        self.first_divisor = 1.4
        #Set the initial divisors
        if self.verbose:
            print('Setting initial divisors...',file=out)
        self.divisors = dict.fromkeys(self.votetotals, self.first_divisor)
        #Initialize dictionary for quotients 
        self.quotients = self.votetotals.copy()
        #self.party_seats_numbers = {}
        self.party_seats_numbers = dict.fromkeys(self.votetotals, 0)

    def distributeseats(self,wait=False,silent=True,verbose=False):

        votetotals_temp = self.votetotals.copy()

        if self.silent:
            out = NullWriter()
        else:
            out = sys.stdout
        
        print('Calculating election result from vote totals for',self.contest.description,file=out)
        print('Number of seats to be distributed: ',self.number_of_seats,file=out)
        print('First divisor:',self.first_divisor,file=out)
        print('Vote totals:',file=out)
        print(self.votetotals,file=out)

        #Calculate initial quotients (divide vote total by first divisor)
        for key in self.quotients:
            self.quotients[key] = self.quotients[key] / self.first_divisor

        
        if self.verbose:
            print('Initial divisors',file=out)
            print(self.divisors)


        while self.awardedseats_total < self.number_of_seats:
            if wait == True:
                print('Ready to award seat #',self.awardedseats_total+1,)
                userinput = input('Press Enter to proceed to next seat. Press E + Enter to proceed to end. ')
                if userinput.lower() == 'e':
                    wait = False
                    print('Input:',userinput)

            if self.verbose:
                print('Awarding seat #',self.awardedseats_total+1,'...',file=out)
            #Award the seat to the party with the highest current quotient
            if self.verbose:
                print('Current quotients:',self.quotients,file=out) 

            #print('DEBUG:self.currentseatwinner',self.currentseatwinner)
            #print('DEBUG:self.votetotals',self.votetotals)
            self.currentseatwinner = max(self.quotients, key=self.quotients.get)

            newseat = CandidateSeat(self.currentseatwinner)
            newseat.winning_quotient = max(self.quotients)
            self.awardedseats.append(newseat)

            self.awardedseats_total  = len(self.awardedseats)

            #Keep track of how many seats won by each party
            self.party_seats_numbers[self.currentseatwinner] = self.party_seats_numbers[self.currentseatwinner] + 1
        
            #Set the new divisor for the seatwinner
            self.divisors[self.currentseatwinner] = 2*self.party_seats_numbers[self.currentseatwinner] + 1

            #Calculate the new quotient for the seatwinner:
            self.quotients[self.currentseatwinner] = self.votetotals[self.currentseatwinner] / self.divisors[self.currentseatwinner]

        print('SEAT DISTRIBUTION FINISHED.',file=out)
        self.status = "Complete"

        return [self.awardedseats,self.party_seats_numbers]

                #Valgoppgjør
    pass



class CandidateSeat(object):
    #mandat
     def __init__(self,seatwinner):
         #self.settlement = settlement
         self.seatwinner = seatwinner
         self.winning_quotient = None


print('DEBUG1')

drammenvalg = Contest('Drammen',57)
#drammenvalg.votetotals = votetotals_drammen
#drammenvalg.votetotals

print('DEBUG2')
drammenvalg.validcontestreport = ContestReport()
drammenvalg.validcontestreport.votetotals = votetotals_drammen
setattr(drammenvalg.validcontestreport,'votetotals',votetotals_drammen)
print('DEBUG3')

print('drammenvalg.validcontestreport.votetotals:',drammenvalg.validcontestreport.votetotals)
result = drammenvalg.perform_settlement()
