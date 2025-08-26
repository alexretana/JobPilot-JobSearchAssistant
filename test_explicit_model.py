from typing import Dict, List
from pydantic import BaseModel, Field

class ExplicitModel(BaseModel):
    top_items: List[Dict[str, int]] = Field(default=[], description="List of items")

# Test creating an ExplicitModel
try:
    model = ExplicitModel(
        top_items=[
            {"name": "Item 1", "count": 10},
            {"name": "Item 2", "count": 20}
        ]
    )
    print("ExplicitModel created successfully!")
    print(model)
except Exception as e:
    print(f"Error creating ExplicitModel: {e}")
    import traceback
    traceback.print_exc()