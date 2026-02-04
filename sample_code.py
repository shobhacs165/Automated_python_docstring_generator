# Missing module docstring → D100
def add(a, b):  # Missing function docstring → D103
    return a + b

def divide(a, b):  # Missing function docstring → D103
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
