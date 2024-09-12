from unittest import TestCase
from more import take, chunked_

class TakeTest(TestCase):
    
    def test_simple_take(self):
        result = take(range(10),5)
        self.assertEqual(result,[0, 1, 2, 3, 4])
        
    def test_simple_take(self):
        result = take(range(10),5)
        self.assertEqual(result,[0, 1, 2, 3, 4])
        
    def test_null_take(self):
        result = take(range(10),0)
        self.assertEqual(result,[])
        
    def test_nagetive_take(self):
        self.assertRaises(ValueError,lambda : take(-3,range(10)))
        
    def test_too_much_take(self):
        result = take(range(5),10)
        self.assertEqual(result,[0, 1, 2, 3, 4])
        
        
class chunkedTest(TestCase):
    
    def test_even(self):
        result = chunked_("ABCDWV",3)
        self.assertEqual(result,[["A","B","C"],["D", "W", "V"]])
        
    def test_odd(self):
        result = chunked_("ABCDW",3)
        self.assertEqual(result,[["A","B","C"],["D", "W"]])
        
    def test_none(self):
        result = chunked_("ABCDW",None)
        self.assertEqual(result,[["A","B","C", "D", "W"]])
        
    def test_strict_false(self):
        result = chunked_("ABCDW",3,strict=False)
        self.assertEqual(result,[["A","B","C"],["D", "W"]])
        
    def test_strict_true(self):
        def f():
            return chunked_("ABCDW",3,strict=True)
        self.assertRaisesRegex(ValueError,"iterator is not dvisible by n", f)
        
    def test_strict_true_size_none(self):
        def f():
            return chunked_("ABCfDW",None,strict=True)
        self.assertRaisesRegex(ValueError,"n cant be None if strict is True", f)