"""
Test suite for The Da Vinci Code implementation
"""

import da_vinci_code


def test_fibonacci_basic():
    """Test basic Fibonacci sequence generation"""
    assert da_vinci_code.fibonacci(0) == []
    assert da_vinci_code.fibonacci(1) == [1]
    assert da_vinci_code.fibonacci(2) == [1, 1]
    assert da_vinci_code.fibonacci(5) == [1, 1, 2, 3, 5]
    assert da_vinci_code.fibonacci(10) == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


def test_golden_ratio():
    """Test Golden Ratio calculation"""
    phi = da_vinci_code.golden_ratio(50)
    # The Golden Ratio should be approximately 1.618033988749895
    assert abs(phi - 1.618033988749895) < 0.0000000000001


def test_decode_message():
    """Test Fibonacci sequence validation"""
    # Valid Fibonacci sequences
    assert da_vinci_code.decode_message([1, 1, 2, 3, 5, 8, 13]) == True
    assert da_vinci_code.decode_message([1]) == True
    assert da_vinci_code.decode_message([1, 1]) == True
    
    # Invalid sequences
    assert da_vinci_code.decode_message([1, 2, 4, 8, 16]) == False
    assert da_vinci_code.decode_message([1, 1, 2, 3, 6]) == False


if __name__ == "__main__":
    # Run all tests
    test_fibonacci_basic()
    print("✓ Fibonacci sequence tests passed")
    
    test_golden_ratio()
    print("✓ Golden Ratio tests passed")
    
    test_decode_message()
    print("✓ Message decoder tests passed")
    
    print("\nAll tests passed successfully! ✓")
