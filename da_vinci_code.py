"""
The Da Vinci Code - Fibonacci Sequence and Golden Ratio

This module implements key mathematical concepts featured in Dan Brown's "The Da Vinci Code":
1. The Fibonacci Sequence - A cryptographic clue in the opening chapters
2. The Golden Ratio (Phi) - A fundamental constant in art and nature
3. Leonardo da Vinci's connection to mathematics and art

The Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...
where each number is the sum of the two preceding numbers.

The Golden Ratio (Phi): approximately 1.618033988749895...
The ratio of consecutive Fibonacci numbers approaches Phi as the sequence progresses.
"""


def fibonacci(n):
    """
    Generate the first n numbers of the Fibonacci sequence.
    
    Args:
        n (int): Number of Fibonacci numbers to generate
        
    Returns:
        list: First n Fibonacci numbers
        
    Example:
        >>> fibonacci(10)
        [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    
    fib_sequence = [1, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    
    return fib_sequence


def golden_ratio(iterations=50):
    """
    Calculate the Golden Ratio (Phi) using the Fibonacci sequence.
    
    As the Fibonacci sequence progresses, the ratio of consecutive numbers
    approaches the Golden Ratio: Phi = (1 + sqrt(5)) / 2 ≈ 1.618033988749895
    
    Args:
        iterations (int): Number of iterations to calculate (default: 50)
        
    Returns:
        float: Approximation of the Golden Ratio
        
    Example:
        >>> phi = golden_ratio(50)
        >>> round(phi, 15)
        1.618033988749895
    """
    fib = fibonacci(iterations)
    if len(fib) < 2:
        return 1.0
    
    # The ratio of consecutive Fibonacci numbers approaches Phi
    return fib[-1] / fib[-2]


def decode_message(sequence):
    """
    A playful homage to the cryptographic puzzles in "The Da Vinci Code".
    Checks if a sequence follows the Fibonacci pattern.
    
    Args:
        sequence (list): A sequence of numbers to validate
        
    Returns:
        bool: True if the sequence is a valid Fibonacci sequence
        
    Example:
        >>> decode_message([1, 1, 2, 3, 5, 8, 13])
        True
        >>> decode_message([1, 2, 3, 4, 5])
        False
    """
    if len(sequence) < 3:
        return True
    
    for i in range(2, len(sequence)):
        if sequence[i] != sequence[i-1] + sequence[i-2]:
            return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("THE DA VINCI CODE - Mathematical Mysteries")
    print("=" * 60)
    print()
    
    # Display the Fibonacci sequence
    print("The Fibonacci Sequence (first 15 numbers):")
    fib_seq = fibonacci(15)
    print(", ".join(map(str, fib_seq)))
    print()
    
    # Calculate and display the Golden Ratio
    phi = golden_ratio(50)
    print(f"The Golden Ratio (Phi): {phi}")
    print(f"Phi (precise to 15 decimals): {phi:.15f}")
    print()
    
    # Demonstrate the convergence to Phi
    print("Convergence of Fibonacci ratios to Phi:")
    fib_convergence = fibonacci(15)
    for i in range(1, len(fib_convergence)):
        ratio = fib_convergence[i] / fib_convergence[i-1]
        print(f"F({i+1})/F({i}) = {fib_convergence[i]}/{fib_convergence[i-1]} = {ratio:.10f}")
    print()
    
    # Test the decoder
    print("Cryptographic Validation:")
    test_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
    print(f"Sequence: {test_sequence}")
    print(f"Valid Fibonacci sequence: {decode_message(test_sequence)}")
    print()
    
    fake_sequence = [1, 2, 4, 8, 16]
    print(f"Sequence: {fake_sequence}")
    print(f"Valid Fibonacci sequence: {decode_message(fake_sequence)}")
    print()
    
    print("=" * 60)
    print('"The Fibonacci sequence is everywhere in nature..."')
    print("                                    - The Da Vinci Code")
    print("=" * 60)
