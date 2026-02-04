"""Calculator module for basic arithmetic operations."""

def add(a, b):
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b


def divide(a, b):
    """Divide two numbers.
    
    Args:
        a: Dividend
        b: Divisor
        
    Raises:
        ValueError: If divisor is zero
        
    Returns:
        Quotient of a divided by b
    """
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
