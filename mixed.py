"""Module for testing mixed documentation coverage and compliance."""

def documented_add(a, b):
    """
    Add two numbers together.
    
    Args:
        a: First number.
        b: Second number.
        
    Returns:
        The sum of a and b.
    """
    return a + b

def undocumented_multiply(a, b):
    # This function has no docstring. 
    # It will decrease both Coverage and Compliance.
    return a * b

class DataProcessor:
    """A class that processes data strings."""
    
    def process(self, data):
        # This method is missing a docstring.
        return data.strip()

def documented_generator(n):
    """
    Generate a sequence of numbers.
    
    Yields:
        int: The next number in the sequence.
    """
    for i in range(n):
        yield i