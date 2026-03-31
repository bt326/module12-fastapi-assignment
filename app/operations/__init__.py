# app/operations.py

"""
Module: operations.py

This module contains basic arithmetic functions that perform addition, subtraction,
multiplication, and division of two numbers. These functions are foundational for
building more complex applications, such as calculators or financial tools.

Functions:
- add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the sum of a and b.
- subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the difference when b is subtracted from a.
- multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the product of a and b.
- divide(a: Union[int, float], b: Union[int, float]) -> float: Returns the quotient when a is divided by b. Raises ValueError if b is zero.

Usage:
These functions can be imported and used in other modules or integrated into APIs
to perform arithmetic operations based on user input.
"""

from typing import Union  # Import Union for type hinting multiple possible types
import logging  

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]


logger = logging.getLogger(__name__)

def add(a: Number, b: Number) -> Number:
    """
    Add two numbers and return the result.
    """
    # Perform addition of a and b
    result = a + b
    logger.info(f"Adding {a} + {b} = {result}")  
    return result

def subtract(a: Number, b: Number) -> Number:
    """
    Subtract the second number from the first and return the result.
    """
    # Perform subtraction of b from a
    result = a - b
    logger.info(f"Subtracting {a} - {b} = {result}")  
    return result

def multiply(a: Number, b: Number) -> Number:
    """
    Multiply two numbers and return the product.
    """
    # Perform multiplication of a and b
    result = a * b
    logger.info(f"Multiplying {a} * {b} = {result}") 
    return result

def divide(a: Number, b: Number) -> float:
    """
    Divide the first number by the second and return the quotient.
    """
    # Check if the divisor is zero to prevent division by zero
    if b == 0:
        logger.error("Cannot divide by zero!")  
        raise ValueError("Cannot divide by zero!")
    
    # Perform division of a by b and return the result as a float
    result = a / b
    logger.info(f"Dividing {a} / {b} = {result}")  
    return result