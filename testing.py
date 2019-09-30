

import settlement
import json
import unittest
import hashlib

test_dict = json.load(open('test_data.json'))
data_dict = json.load(open('data.json'))

votetotals_drammen = data_dict["Drammen"]["voteTotals"].copy()
test_result = settlement.distribute_seats_wrapper(data_dict,"Drammen")

class TestJson(unittest.TestCase):

    #def setUp(self):
    #    data_dict = json.load(open('data.json'))
    #    test_dict = json.load(open('test_data.json'))

    def testvalidJSON(self):
        
        
        self.assertEqual(type(json.load(open('data.json'))),type({}))

    #def testbadJSON(self):
    #    self.assertEqual(type(json.load(open('invalid.json'))),type({}))
    


class TestWrapDistributeSeats(unittest.TestCase):
    def setUp(self):
        test_result = settlement.distribute_seats_wrapper(data_dict,"Drammen")

    def TestResultIsList(self):
        self.assertEqual(type(test_result),type([]))

class TestDistributeSeats(unittest.TestCase):

    #def setUp(self):
        #test_dict = json.load(open('test_data.json'))

    def test_distribute_seats_result(self):
        #Note: Tests will fail if party names are changed
        result = settlement.distribute_seats(votetotals_drammen,57,silent = True)
        result[0].sort()
        seats_string = str(result[0]).encode('utf-8')
        returned_seats_hash = hashlib.sha256()
        returned_seats_hash.update(seats_string)
        self.assertEqual(returned_seats_hash.hexdigest(),'20d3f16653c2691b15dfba96538a84a76872317c3dcae094f404d4281af37d6c') #Doesn't work, hash changes every time.

        result[1].sort()
        winning_quotient_divisors_string = str(result[1]).encode('utf-8')
        returned_winning_quotient_divisors =  hashlib.sha256()
        returned_winning_quotient_divisors.update(winning_quotient_divisors_string)
        returned_winning_quotient_divisors.hexdigest()
        self.assertEqual(returned_winning_quotient_divisors.hexdigest(),'e5ef711bf14883fc4b68bcd072206bef19938a24936133d7df03e3c7334471c7')
        #self.assertEqual(hash(str(result[2])),698152000) 
        #self.assertEqual(hash(str(result[3])),-1510847281)

    def test_equal_vote_totals(self):
        result = settlement.distribute_seats_wrapper(test_dict,"equal_votetotals_test1")
        self.assertEqual(result[0],['A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A'])
        self.assertEqual(result[1],[1.4, 1.4, 1.4, 3, 3, 3, 5, 5, 5, 7])
        self.assertEqual(result[2],[53255.71428571429, 38205.0, 38205.0, 24852.666666666668, 17829.0, 17829.0, 14911.6, 10697.4, 10697.4, 10651.142857142857])

    def test_equal_ballot_numbers(self):
        result = settlement.distribute_seats_wrapper(test_dict,"equal_votetotals_test2")
        self.assertEqual(result,None)


class TestLeastVoteChange(unittest.TestCase):

    def test_invalid_count_type(self):
        self.assertEqual(settlement.leastvotechange(votetotals_drammen,57,'Invalid count type'),None)

    #def test_listestemmetall(self):


#    def test_stemmer(self):

class TestCompareResults(unittest.TestCase):
    def test_compare_results(self):
        self.assertEqual(settlement.compareresults(test_result,test_result),True)

if (__name__ == '__main__'):
    unittest.main()
