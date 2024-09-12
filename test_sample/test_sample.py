import unittest 
from sample import divide ,Person

class divideTest(unittest.TestCase):
    def setUp(self):
        self.divide1 = divide(4,2)
        self.divide2 = divide(4,2)
        
    def test_divide(self):
        self.assertEqual(self.divide1,2)
        
    def test_divide(self):
        self.assertRaises(ZeroDivisionError,divide ,4, 0)

class PersonTest(unittest.TestCase):
    def setUp(self):
        self.p1 = Person("Ali","Ahmadi")
        self.p2 = Person("MM", "NNNOORR")
    
    def tearDown(self):
        print("Done")
    
    def test_fullname(self):
        self.assertEqual(self.p1.fullname(),"Ali Ahmadi")


if __name__ == '__main__':
    unittest.main()
    
    
# python m unittest test_sample.py
# python -m unittest discover  --> in root start file test_ run test