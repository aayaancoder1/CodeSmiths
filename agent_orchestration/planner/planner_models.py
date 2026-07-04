import sys
from typing import Dict, Any, List

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Shim to support environments without pydantic installed
    import dataclasses

    def Field(default=None, **kwargs):
        # Return default value directly for compatibility with standard class attributes
        return default

    class BaseModel:
        def __init__(self, **kwargs):
            # Set values
            for name, val in kwargs.items():
                setattr(self, name, val)
            # Ensure defaults for fields that are missing
            for name, field_type in getattr(self, '__annotations__', {}).items():
                if name not in kwargs:
                    # Check class attribute for default
                    if hasattr(self.__class__, name):
                        default_val = getattr(self.__class__, name)
                        # If it's a factory (like list or dict), create a new instance
                        if default_val == list or (isinstance(default_val, list) and not default_val):
                            setattr(self, name, [])
                        elif default_val == dict or (isinstance(default_val, dict) and not default_val):
                            setattr(self, name, {})
                        else:
                            setattr(self, name, default_val)
                    else:
                        setattr(self, name, None)

        def dict(self) -> Dict[str, Any]:
            return self._to_dict(self)

        def model_dump(self) -> Dict[str, Any]:
            return self._to_dict(self)

        def _to_dict(self, obj: Any) -> Any:
            if isinstance(obj, BaseModel):
                return {k: self._to_dict(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [self._to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: self._to_dict(v) for k, v in obj.items()}
            return obj

# Define the models using Pydantic (or the shim)
class TaskNode(BaseModel):
    task_id: str
    tool_id: str
    dependencies: List[str] = list
    inputs: Dict[str, Any] = dict
    confirmation_required: bool = False
    description: str = ""

class WorkflowMetadata(BaseModel):
    workflow_id: str
    goal: str
    estimated_steps: int
    created_at: str

class ExecutionPlan(BaseModel):
    workflow_id: str
    goal: str
    steps: List[TaskNode]
    confirmation_required: bool
    tool_requirements: List[str]
    expected_result: str
    metadata: Dict[str, Any] = dict

class PlannerResult(BaseModel):
    workflow_id: str
    execution_plan: ExecutionPlan
    ordered_task_graph: Dict[str, List[str]]
    confirmation_flag: bool
    tool_requirements: List[str]
    estimated_execution_order: List[str]
