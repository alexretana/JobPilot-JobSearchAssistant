from typing import Dict
from pydantic import BaseModel

class VerySimpleModel(BaseModel):
    items: Dict[str, int] = {}

# Test creating a VerySimpleModel
try:
    model = VerySimpleModel(
        items={
            "item1": 10,
            "item2": 20
        }
    )
    print("VerySimpleModel created successfully!")
    print(model)
except Exception as e:
    print(f"Error creating VerySimpleModel: {e}")
    import traceback
    traceback.print_exc()