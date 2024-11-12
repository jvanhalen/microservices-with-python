from fastapi.testclient import TestClient
import pytest
from app.stack.main import app  # Import your FastAPI app

client = TestClient(app)

def test_push_item_endpoint():
    """Test pushing an item onto the stack."""
    response = client.post("/push/", json={"item": "Hello"})
    assert response.status_code == 200
    assert response.json()["message"] == "Item pushed successfully"
    assert response.json()["stack_size"] == 1  # Stack size should be 1 after push

def test_pop_item_endpoint():
    """Test popping an item from the stack."""
    # Now pop the item
    response = client.post("/pop/")
    assert response.status_code == 200
    assert response.json()["message"] == "Item popped successfully"
    assert response.json()["item"] == "Hello"
    assert response.json()["stack_size"] == 0  # Stack size should be 0 after pop

def test_pop_empty_stack_endpoint():
    """Test popping an item from an empty stack."""
    # Try to pop an item from an empty stack
    response = client.post("/pop/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Stack is empty"  # Ensure the error message matches

def test_stack_size_endpoint():
    """Test getting the stack size."""
    # Push two items onto the stack
    client.post("/push/", json={"item": "Hello"})
    client.post("/push/", json={"item": "World"})
    
    # Now check the stack size
    response = client.get("/size/")
    assert response.status_code == 200
    assert response.json()["stack_size"] == 2  # Stack size should be 2
