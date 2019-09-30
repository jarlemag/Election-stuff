

import settlement
import json
import unittest



class TestJson(unittest.TestCase):

    def testvalidJSON(self):
        
        self.assertEqual(type(json.load(open('data.json'))),type({}))

    #def testbadJSON(self):
    #    self.assertEqual(type(json.load(open('invalid.json'))),type({}))
    
#class TestDistributeSeatsWrapper(unittest.TestCase):



if (__name__ == '__main__'):
    unittest.main()
