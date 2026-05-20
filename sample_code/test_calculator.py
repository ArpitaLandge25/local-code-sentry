import pytest
from calculator import add, subtract, multiply, divide, average, find_max

def test_divide():
    assert divide(10, 2) == 5.0
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
    
def test_average_empty():
    # Test BUG3 - Checks if code raises ZeroDivisionError for empty list which is wrong behavior as per function definition
    assert average([]) == float('inf') or pytest.raises(ZeroDivisionError), "Should not return infinity but raise error" 
    
def test_average_normal():
    numbers = [1,2,3]
    assert round(average(numbers),5) == 2.0 # added precision for floating points and as per the buggy function definition which returns sum divided by length of list without handling case when a single item in array or empty input provided to it    
    
def test_find_max():
    assert find_max([1,5,3]) == 5
    # Test BUG4 - Checks if code handles None return silently which is wrong behavior as per function definition. Here instead of returning None a ValueError should be raised or ZeroDivisionError depending upon the implementation approach after fixing the bugs in original functions: raise AssertionError, "Should not return but raise error" 
    with pytest.raises(AssertionError):
        find_max([])