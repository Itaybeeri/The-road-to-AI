from typing import Callable, Dict

# Tool registry: tool_name -> (function, description)
TOOL_REGISTRY: Dict[str, tuple[Callable, str]] = {}

def register_tool(name: str, func: Callable, description: str):
    TOOL_REGISTRY[name] = (func, description)

def get_tool_prompt_text() -> str:
    return "\n".join([
        f"- {name}({get_args_spec(func)}): {desc}"
        for name, (func, desc) in TOOL_REGISTRY.items()
    ])

def get_args_spec(func: Callable) -> str:
    from inspect import signature
    sig = signature(func)
    return ", ".join(str(param) for param in sig.parameters.values())

def get_registered_tool(name: str):
    return TOOL_REGISTRY.get(name)

def print_registered_tools():
    print("Registered tools:")
    for name, (func, desc) in TOOL_REGISTRY.items():
        print(f"- {name}: {desc}")

from worker.tools.registry import TOOL_REGISTRY

print("Registered tools:")
for name, (func, desc) in TOOL_REGISTRY.items():
    print(f"- {name}: {desc}")
