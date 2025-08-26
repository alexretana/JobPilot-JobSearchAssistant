from typing import Dict, List
from pydantic import BaseModel

class SimpleModel(BaseModel):
    top_items: List[Dict[str, int]] = []

# Test creating a SimpleModel
try:
    model = SimpleModel(
        top_items=[
            {"name": "Item 1", "count": 10},
            {"name": "Item 2", "count": 20}
        ]
    )
    print("SimpleModel created successfully!")
    print(model)
except Exception as e:
    print(f"Error creating SimpleModel: {e}")
    import traceback
    traceback.print_exc()