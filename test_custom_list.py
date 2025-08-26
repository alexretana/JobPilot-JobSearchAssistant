from typing import List
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    count: int

class CustomListModel(BaseModel):
    top_items: List[Item] = []

# Test creating a CustomListModel
try:
    model = CustomListModel(
        top_items=[
            Item(name="Item 1", count=10),
            Item(name="Item 2", count=20)
        ]
    )
    print("CustomListModel created successfully!")
    print(model)
except Exception as e:
    print(f"Error creating CustomListModel: {e}")
    import traceback
    traceback.print_exc()