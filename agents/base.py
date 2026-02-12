from typing import List, Dict, Any, Optional
import json

class BaseAgent:
    def __init__(self, name: str, role: str, goal: str, backstory: str = ""):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.memory: List[Dict[str, Any]] = []
        self.tools: Dict[str, Any] = {}

    def add_tool(self, name: str, func: callable):
        """Register a tool available to this agent."""
        self.tools[name] = func

    def think(self, context: Any) -> str:
        """
        Simulate the agent's reasoning process. 
        In a real LLM integration, this would call the model.
        For now, it returns a log of the intent.
        """
        return f"[{self.name}] Thinking about: {str(context)[:50]}..."

    def act(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found for {self.name}")
        
        print(f"[{self.name}] Executing {tool_name} with args: {kwargs}")
        return self.tools[tool_name](**kwargs)

    def run(self, input_data: Any) -> Any:
        """Main entry point for the agent's task."""
        raise NotImplementedError("Subclasses must implement run()")

    def __repr__(self):
        return f"<Agent {self.name}: {self.role}>"
