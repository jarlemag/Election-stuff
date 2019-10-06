import settlement
import json
import unittest
import hashlib

from electionclasses import *

test_dict = json.load(open('test_data.json'))
data_dict = json.load(open('data.json'))

votetotals_drammen = data_dict["Drammen"]["voteTotals"].copy()
test_result = settlement.distribute_seats_wrapper(data_dict,"Drammen",silent = True)



drammenvalg = Contest('Drammen',57)
drammenvalg.validcontestreport = ContestReport()
drammenvalg.validcontestreport.votetotals = votetotals_drammen
setattr(drammenvalg.validcontestreport,'votetotals',votetotals_drammen)


print('drammenvalg.validcontestreport.votetotals:',drammenvalg.validcontestreport.votetotals)
result = drammenvalg.perform_settlement()


print('result:',result)
print('DebugB')


class TestSettlement(unittest.TestCase):


    def testDistributeSeats_result(self):
        #Note: Tests will fail if party names are changed
        #result = settlement.distribute_seats(votetotals_drammen,57,silent = True)
        result=drammenvalg.result

        #print('DEBUG:',result[0])

        seats = [value.seatwinner for value in result[0]]
        seats.sort()
        seats_string = str(seats).encode('utf-8')
        returned_seats_hash = hashlib.sha256()
        returned_seats_hash.update(seats_string)
        self.assertEqual(returned_seats_hash.hexdigest(),'20d3f16653c2691b15dfba96538a84a76872317c3dcae094f404d4281af37d6c')

        #result[1].sort()
        #winning_quotient_divisors_string = str(result[1]).encode('utf-8')
        #returned_winning_quotient_divisors =  hashlib.sha256()
        #returned_winning_quotient_divisors.update(winning_quotient_divisors_string)
        #self.assertEqual(returned_winning_quotient_divisors.hexdigest(),'e5ef711bf14883fc4b68bcd072206bef19938a24936133d7df03e3c7334471c7')


        #result[2].sort()
        #winning_quotients_string = str(result[2]).encode('utf-8')
        #returned_winning_quotients = hashlib.sha256()
        #returned_winning_quotients.update(winning_quotients_string)
        #self.assertEqual(returned_winning_quotients.hexdigest(),'63bd2b56273b998f04799bb717d45a8298f39b6557cdd56b68e5a610e258ef63') 

        
        party_seats_numbers_string = str(result[1]).encode('utf-8')
        returned_party_seats_numbers = hashlib.sha256()
        returned_party_seats_numbers.update(party_seats_numbers_string)
        self.assertEqual(returned_party_seats_numbers.hexdigest(),'cb20838c2bb442e37a04ee748844e9bd0cb96686a27e86d7dddaceb96791636d')
        
    def test_equal_vote_totals(self):
        pass

    def test_equal_ballot_numbers(self):
        pass



class TestLeastVoteChange(unittest.TestCase):
    pass


if (__name__ == '__main__'):
    unittest.main()
