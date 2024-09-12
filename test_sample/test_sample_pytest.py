import pytest 
from sample import divide ,Person
import time

class Testdivide:
    @pytest.fixture
    def fixture_setup(self):
        self.divide1 = divide(4,2)
        self.divide2 = divide(4,2)
        
    def test_divide(self,fixture_setup):
        assert self.divide1==2
        
    def test_divide(self):
        with pytest.raises(ZeroDivisionError):
            divide(4,0)

class TestPerson: # start name class with Test
    @pytest.fixture
    def fixture_setup(self):
        self.p1 = Person("Ali","Ahmadi")
        self.p2 = Person("MM", "NNNOORR")
        yield 'fixture_setup'
        # after yield --> tear_down
        print("Done") # ---> dont work in teardown pytest 
        time.sleep(2)

        
    def test_fullname(self,fixture_setup):
        assert self.p1.fullname()=="Ali Ahmadi"

    
    
# pytest test_sample.py
# pytest discover  --> in root start file test_ run test
# pytest name_file.py --resultlog=result.log