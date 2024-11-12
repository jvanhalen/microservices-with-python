import pytest
from app.stack.main import Stack  # Import your FastAPI app and Stack class

# Create a fixture with scope="function" to ensure the stack is reset for every test
@pytest.fixture(scope="function")
def stack():
    return Stack()  # Return a fresh instance of the Stack for each test

# Test function to check pushing an item onto the stack
def test_push(stack):
    assert len(stack) == 0  # Initially, stack should be empty
    stack.push("hello")
    assert len(stack) == 1  # Stack size should be 1 after push
    stack.push("world")
    assert len(stack) == 2  # Stack size should be 2 after push

# Test function to check popping an item from the stack
def test_pop(stack):
    stack.push("hello")
    stack.push("world")
    assert stack.pop() == "world"  # Last item should be popped first (LIFO)
    assert stack.pop() == "hello"  # The next item should be popped
    assert stack.pop() is None  # The stack should be empty, so pop returns None

# Test function to ensure the stack is empty after popping all items
def test_stack_empty_after_pop(stack):
    stack.push("item1")
    stack.push("item2")
    stack.pop()  # Removes item2
    stack.pop()  # Removes item1
    assert len(stack) == 0  # Stack should be empty
    assert stack.pop() is None  # Popping from an empty stack should return None