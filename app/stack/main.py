from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional

app = FastAPI()

class Stack:
    """A basic LIFO stack class with push and pop operations."""
    def __init__(self) -> None:
        """Initializes an empty stack."""
        self._storage = []

    def __len__(self) -> int:
        """Returns the number of items in the stack."""
        return len(self._storage)

    def push(self, item: Any) -> None:
        """Pushes a new item onto the top of the stack."""
        self._storage.append(item)

    def pop(self) -> Optional[Any]:
        """Pops and returns the item from the top of the stack."""
        if self._storage:
            return self._storage.pop()
        else:
            return None

# Create a global stack instance
stack = Stack()

# Define a Pydantic model for input data
class ItemModel(BaseModel):
    item: Any

@app.post("/push/")
async def push_item(item: ItemModel):
    """Push an item onto the stack."""
    stack.push(item.item)
    return {"message": "Item pushed successfully", "stack_size": len(stack)}

@app.post("/pop/")
async def pop_item():
    """Pop an item from the stack."""
    item = stack.pop()
    if item is None:
        raise HTTPException(status_code=404, detail="Stack is empty")
    return {"message": "Item popped successfully", "item": item, "stack_size": len(stack)}

@app.get("/size/")
async def stack_size():
    """Get the current size of the stack."""
    return {"stack_size": len(stack)}

# TODO: implement this please! :)
@app.get("/stack/")
async def get_stack():
    """Retrieve the current items in the stack."""
    # Returning the entire stack storage for reference (without modifying it)
    return {"message": "not implemented yet!", "stack": stack._storage}