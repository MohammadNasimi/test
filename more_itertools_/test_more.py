from unittest import TestCase
from more import *
import traceback

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
        
    # def test_strict_true(self):
    #     def f():
    #         return chunked_("ABCDW",3,strict=True)
    #     self.assertRaisesRegex(ValueError,"iterator is not dvisible by n", f)
        
    def test_strict_true_size_none(self):
        def f():
            return chunked_("ABCfDW",None,strict=True)
        self.assertRaisesRegex(ValueError,"n cant be None if strict is True", f)
        
        
class FirstTest(TestCase):
    
    def test_many(self):
        self.assertEqual(first(x for x in range(4)), 0)
            
    def test_one(self):
        self.assertEqual(first([3]), 3)
        
    def test_default(self):
        self.assertEqual(first([],"a"), "a")
                         
    def test_emptry_stopiterations(self):
        try:
            first([])
        except ValueError:
            formatted_exe = traceback.format_exc()
            print("**"*50)
            print(formatted_exe)
            self.assertIn("StopIteration", formatted_exe)                    
            self.assertIn("first() was called on an empty iterable", formatted_exe)
        else:
            self.fail()                    
            
        
class LastTests(TestCase):
    def test_basic(self):
        cases = [
            (range(4),3),
            (iter(range(4)),3),
            (range(1),0),
            (iter(range(1)),0),
            ({n:str(n) for n in range(5)},4)
        ]
        for iterable , expected in cases:
            with self.subTest(iterable):
                self.assertEqual(last(iterable),expected)
                
    def test_default(self):
        for iterable, defualt, expected in [
            (range(1),None, 0),
            ([], None, None),
            ({}, None, None),
            (iter([]), None, None)
        ]:
            with self.subTest(args=(iterable,defualt)):
                self.assertEqual(last(iterable,defualt),expected)
                
    def test_emptry(self):
        for iterable in ([],iter(range(0))):
            with self.subTest(iterable):
                with self.assertRaises(ValueError):
                    last(iterable)   
            
            
class NthOrLastTest(TestCase):
    def test_basic(self):
        self.assertEqual(nth_or_last(range(3), 1),1)
        self.assertEqual(nth_or_last(range(3), 3),2) # [0, 1, 2]
    
    def test_default(self):
        default = 42
        self.assertEqual(nth_or_last(range(0),3,default),default)
        
    def test_emptry(self):
        self.assertRaises(ValueError,lambda: nth_or_last(range(0),1))