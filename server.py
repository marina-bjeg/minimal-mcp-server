# server.py
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("hello-world")
 
# TOOL: say_hello(name) -> "Hello, <name>!"
@mcp.tool()
def say_hello(name: str) -> str:
    """Greets a person by name."""
    return f"Hello, {name}!"
 
# RESOURCE: hello://{name} -> text payload
@mcp.resource("hello://{name}")
def hello_resource(name: str) -> str:
    """Dynamic greeting resource."""
    return f"Hello (resource), {name}!"
 
# PROMPT: hello_prompt(name) -> reusable prompt text
@mcp.prompt()
def hello_prompt(name: str) -> str:
    """A prompt template that politely greets someone."""
    return f"Please greet {name} politely."
 
if __name__ == "__main__":
    # STDIO is the default transport; perfect for VS Code/Copilot
    mcp.run()