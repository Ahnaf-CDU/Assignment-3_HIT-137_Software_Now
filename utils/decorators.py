"""
Custom Decorators - Demonstrates Multiple Decorators

OOP Concepts Used:
1. Decorators: Functions that modify behavior of other functions
2. Multiple Decorators: Stacking decorators on functions
3. Functional Programming: Higher-order functions
"""

import time
import functools


def log_execution(func):
    """
    Decorator to log function execution
    Demonstrates decorator pattern
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executing: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Completed: {func.__name__}")
        return result
    return wrapper


def timer(func):
    """
    Decorator to measure execution time
    Demonstrates decorator pattern
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"[TIMER] {func.__name__} took {execution_time:.4f} seconds")
        return result
    return wrapper


def validate_input(input_type=str):
    """
    Decorator to validate input types
    Demonstrates parameterized decorator
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if first argument (after self) matches expected type
            if len(args) > 1 and not isinstance(args[1], input_type):
                raise TypeError(f"{func.__name__} expects {input_type.__name__}, got {type(args[1]).__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def error_handler(default_return=None):
    """
    Decorator to handle errors gracefully
    Demonstrates error handling in decorators
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR] {func.__name__} failed: {e}")
                return default_return
        return wrapper
    return decorator


def cache_result(func):
    """
    Decorator to cache function results
    Demonstrates memoization pattern
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"[CACHE] Returning cached result for {func.__name__}")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


# Example of using multiple decorators
@timer
@log_execution
def example_function():
    """
    Example function demonstrating multiple decorators
    Shows how decorators can be stacked
    """
    time.sleep(0.1)
    return "Example completed"


if __name__ == "__main__":
    # Test decorators
    print("Testing decorators...")
    result = example_function()
    print(f"Result: {result}")
