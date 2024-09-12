from sample import divide ,Person

# you dont need import nose 
        
def test_divide1():
    assert divide(4,2)==2
    assert divide(4,4)!=2
        
def test_divide2():
    assert divide(4,0)==ZeroDivisionError


    
    
# nosetests -v test_sample_nose.py


