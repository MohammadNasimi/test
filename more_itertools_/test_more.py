from unittest import TestCase
from more import *
import traceback
from time import sleep
from itertools import count,cycle

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
        

class OneTest(TestCase):
    def test_basic(self):
        self.assertEqual(one(["hello"]),"hello")
    
    def test_too_short(self):
        it = []
        for too_short, exc_type in [
            # (None,ValueError)
            (IndexError,IndexError)   
        ]:
            with self.subTest(too_short):
                try:
                    one(it,too_short=too_short)
                except exc_type:
                    formated_exec = traceback.format_exc()
                    self.assertIn("StopIteration", formated_exec)
                    self.assertIn("The above exception was the direct cause", formated_exec)
                else:
                    self.fail()
        
    def test_too_long(self):
        it = count()
        self.assertRaises(ValueError,lambda: one(it))
        self.assertEqual(next(it),2)
        self.assertRaises(OverflowError,lambda: one(it,too_long=OverflowError))
    
    # def test_too_long_default_message(self):
    #     it =[0,1]
    #     self.assertRaises(ValueError,"expected exactly one item in iterable, but got 0,1 , and perhaps more.",lambda: one(it))
    
class InterLeaveTest(TestCase):
    def test_even(self):
        actual = interleave([1,4,7],[2,5,8],[3,6,9])
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(actual, expected)

    def test_short(self):
        actual = interleave([1,4],[2,5,8],[3,6])
        expected = [1, 2, 3, 4, 5, 6]
        self.assertEqual(actual, expected)
        
    def test_mixed_types(self):
        it_list = ['a','b','c','d']
        it_str = '123456'
        it_inf = count()
        actual = interleave(it_list,it_str,it_inf)
        expected = ['a','1',0,'b','2',1,'c','3',2,'d','4',3]
        self.assertEqual(actual, expected)


class RepeatEachTest(TestCase):
    def test_default(self):
        actual = list(repeat_each("ABCD"))
        expected = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D']
        self.assertEqual(actual, expected)
        
    def test_basic(self):
        actual = list(repeat_each("ABCD",3))
        expected = ['A', 'A','A', 'B', 'B','B', 'C', 'C','C', 'D', 'D','D']
        self.assertEqual(actual, expected)
    
    def test_empty(self):
        actual = list(repeat_each(""))
        expected = []
        self.assertEqual(actual, expected)
        
    def test_no_repeat(self):
        actual = list(repeat_each("ABC",0))
        expected = []
        self.assertEqual(actual, expected)
        
    def test_negative_repeat(self):
        actual = list(repeat_each("ABC",-1))
        expected = []
        self.assertEqual(actual, expected)
        
    def test_infinitive_repeat(self):
        repeater = repeat_each(cycle("AB"))
        actual = take(repeater,6)
        expected = ['A', 'A', 'B', 'B','A', 'A']
        self.assertEqual(actual, expected)
        
        
        
class Strictly_NTest(TestCase):
    def test_negative_repeat(self):
        iterable = ['a','b','c','d']
        n=4
        actual = list(strictly_n(iterable,n))
        expected = ['a','b','c','d']
        self.assertEqual(actual, expected)  
        
    def test_too_short(self):
        iterable = ['a','b','c','d']
        n=5
        with self.assertRaises(ValueError) as e:
            list(strictly_n(iterable,n)) 
            
        self.assertEqual(
            "Too few items in iterable got 4", e.exception.args[0]
        )
    def test_too_long(self):
        iterable = ['a','b','c','d']
        n=3
        with self.assertRaises(ValueError) as e:
            list(strictly_n(iterable,n)) 
            
        self.assertEqual(
            "Too many items in iterable got 4", e.exception.args[0]
        )
        
    def test_too_short_custom(self):
        call_count = 0
        def too_short(item_count):
            nonlocal call_count # use call_count variable in function
            call_count +=1
        
        iterable = ['a','b','c','d']
        n=6
        actual = []
        
        for item in strictly_n(iterable,n,too_short=too_short):
            actual.append(item)
        expected = ['a','b','c','d']
        self.assertEqual(actual, expected)  
        self.assertEqual(call_count, 1)  
        
        
class AlwaysRerviersibleTest(TestCase):
    def test_regular_reversed(self):
        self.assertEqual(list(reversed(range(10))),list(always_reversible(range(10))))
        self.assertEqual(list(reversed([1,2,3])),list(always_reversible([1,2,3])))
        self.assertEqual(reversed([1,2,3]).__class__,always_reversible([1,2,3]).__class__)
        
    def test_nonsequence_reversed(self):
        self.assertEqual(list(reversed(range(10))),list(always_reversible(x for x in range(10))))
        self.assertEqual(list(reversed([1,2,3])),list(always_reversible(x for x in [1,2,3])))
        self.assertEqual(reversed([1,2,3]).__class__,always_reversible(x for x in [1,2,3]).__class__)
        
class SplitAfterTest(TestCase):
    def test_start_with_sep(self):
        actual = list(split_after('xooxoo',lambda c: c=="x"))
        expected = [['x'], ['o','o','x'], ['o','o']]
        self.assertEqual(actual, expected)
        
    def test_no_sep(self):
        actual = list(split_after('oooo',lambda c: c=="x"))
        expected = [['o','o','o','o']]
        self.assertEqual(actual, expected)

class SplitIntoTest(TestCase):
    def test_iterable_just_right(self):
        iterable = [1,2,3,4,5,6,7,8,9]
        sizes = [2,3,4]
        actual = list(split_into(iterable,sizes))
        expected = [[1,2], [3,4,5], [6,7,8,9]]
        self.assertEqual(actual, expected)
        
    def test_iterable_too_small(self):
        iterable = [1,2,3,4,5,6,7]
        sizes = [2,3,4]
        actual = list(split_into(iterable,sizes))
        expected = [[1,2], [3,4,5], [6,7]]
        self.assertEqual(actual, expected)
        
    def test_iterable_too_small_extra(self):
        iterable = [1,2,3,4,5,6,7]
        sizes = [2,3,4,5]
        actual = list(split_into(iterable,sizes))
        expected = [[1,2], [3,4,5], [6,7], []]
        self.assertEqual(actual, expected)
        
    def test_iterable_too_large(self):
        iterable = [1,2,3,4,5,6,7,8,9]
        sizes = [2,3,2]
        actual = list(split_into(iterable,sizes))
        expected = [[1,2], [3,4,5], [6,7]]
        self.assertEqual(actual, expected)
        
    def test_iterable_too_small_extra(self):
        iterable = [1,2,3,4,5,6,7,8,9]
        sizes = [2,3,None]
        actual = list(split_into(iterable,sizes))
        expected = [[1,2], [3,4,5], [6,7,8,9]]
        self.assertEqual(actual, expected)
        
        
    def test_iterable_none_mid_sizes(self):
        iterable = [1,2,3,4,5,6,7,8,9]
        sizes = [2,3,None,3]
        actual = list(split_into(iterable,sizes))
        expected = [[1,2], [3,4,5], [6,7,8,9]]
        self.assertEqual(actual, expected)
        
    def test_iterable_empty(self):
        iterable = []
        sizes = [2,3,3]
        actual = list(split_into(iterable,sizes))
        expected = [[], [], []]
        self.assertEqual(actual, expected)
        
    def test_iterable_emoty_using_none(self):
        iterable = []
        sizes = [2,3,None,3]
        actual = list(split_into(iterable,sizes))
        expected = [[], [], []]
        self.assertEqual(actual, expected)
        
    def test_sizes_empty(self):
        iterable = [1,2,3,4,5,6,7,8,9]
        sizes = []
        actual = list(split_into(iterable,sizes))
        expected = []
        self.assertEqual(actual, expected)
        
    def test_both_empty(self):
        iterable = []
        sizes = []
        actual = list(split_into(iterable,sizes))
        expected = []
        self.assertEqual(actual, expected)
        
        

class MapIfTest(TestCase):
    def test_with_out_func_else(self):
        iterable = list(range(-5,5))
        actual = list(map_if(iterable,lambda x: x>3,lambda x: "TooBig"))
        expected = [-5,-4,-3,-2,-1,0,1,2,3,"TooBig"]
        self.assertEqual(actual, expected)
        
    def test_with_func_else(self):
        iterable = list(range(-5,5))
        actual = list(map_if(iterable,lambda x: x>=0,lambda x: "notneg",lambda x:'neg'))
        expected = ['neg','neg','neg','neg','neg',"notneg","notneg","notneg","notneg","notneg"]
        self.assertEqual(actual, expected)
        
        
class TimeLimitedTests(TestCase):
    def test_basic(self):
        def generator():
            yield 1
            yield 2
            sleep(0.2)
            yield 3
            
        iterable = time_limited(0.1,generator())
        actual = list(iterable)
        expected = [1,2]
        self.assertEqual(actual,expected)
        
        
class SequenceView(TestCase):
    def test_init(self):
        view = SequenceView([1,2,3])
        self.assertEqual(repr(view),"SequenceView((1,2,3))")
        self.assertRaises(TypeError , lambda : SequenceView({}))