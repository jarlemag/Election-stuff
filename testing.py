

import settlement
import json
import unittest

test_dict = json.load(open('test_data.json'))
data_dict = json.load(open('data.json'))

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

    def test_equal_vote_totals(self):
        result = settlement.distribute_seats_wrapper(test_dict,"equal_votetotals_test1")
        self.assertEqual(result[0],['A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A'])
        self.assertEqual(result[1],[1.4, 1.4, 1.4, 3, 3, 3, 5, 5, 5, 7])
        self.assertEqual(result[2],[53255.71428571429, 38205.0, 38205.0, 24852.666666666668, 17829.0, 17829.0, 14911.6, 10697.4, 10697.4, 10651.142857142857])

    def test_equal_ballot_numbers(self):
        result = settlement.distribute_seats_wrapper(test_dict,"equal_votetotals_test2")
        self.assertEqual(result,None)



if (__name__ == '__main__'):
    unittest.main()
