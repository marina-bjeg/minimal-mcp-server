# minimal-mcp-server

`minimal-mcp-server` is a tiny, open MCP server you can copy, extend, or embed. It shows a minimal viable set of MCP concepts (tool, dynamic resource, prompt) over stdio for Copilot / editor integration.

## Features

* Tool: `say_hello(name)` → returns greeting
* Resource: `hello://{name}` dynamic text
* Prompt: `hello_prompt(name)` template
* Transport: stdio (works with VS Code / Copilot MCP)

## Quick Start

```powershell
irm https://astral.sh/uv/install.ps1 | iex
git clone <REPO_URL> minimal-mcp-server
cd minimal-mcp-server
uv venv
uv pip install -e .
uv run mcp run server.py
```

Then in VS Code → Copilot → Configure Tools → ensure it lists `minimal-mcp-server`.

## Prerequisites

* Python 3.11+
* `uv` (single binary recommended)

### Install uv

Recommended (PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Alternative (pip):

```powershell
pip install uv
```

## Environment Setup

```powershell
uv venv                 # creates .venv
uv pip install -e .     # installs mcp[cli] + this project editable
```

Optional manual activation (not required when using `uv run`):

```powershell
. .\.venv\Scripts\Activate.ps1
```

## Run Locally

```powershell
uv run mcp run server.py
```

If you see a Typer error, ensure dependency is `mcp[cli]` (already defined in `pyproject.toml`).

## VS Code / Copilot Integration

`.vscode/mcp.json` (already included):

```jsonc
{
  "servers": {
     "minimal-mcp-server": {
        "type": "stdio",
        "command": "uv",
        "args": ["run", "mcp", "run", "${workspaceFolder}/server.py"]
     }
  }
}
```

Then: Copilot → Configure Tools → ensure `minimal-mcp-server` appears (add if needed).

## Using the Tool

Call tool `say_hello` with payload `{ "name": "David" }` → `Hello, David!`.

Resource request example: `hello://Maria` → `Hello (resource), Maria!`

Prompt template: `hello_prompt` with `{ "name": "Ana" }` → prompt text.

## Available Tools

| Name       | Kind    | Description                       | Parameters                    | Example Invocation (args)              | Example Result        |
|------------|---------|-----------------------------------|--------------------------------|----------------------------------------|-----------------------|
| say_hello  | tool    | Returns a greeting for a given name | name: string (required)       | `{ "name": "Andrei" }`                | `Hello, Andrei!`      |
| hello://{name} | resource | Dynamic greeting resource        | path variable: name           | `hello://Marina`                       | `Hello (resource), Marina!` |
| hello_prompt | prompt | Produces a polite greeting prompt | name: string (required)       | `{ "name": "Team" }` (prompt request) | `Please greet Team politely.` |

Notes:

* Tools are invoked via the MCP tool call interface.
* Resources are fetched by requesting the URI.
* Prompts return a template string you can feed into an LLM.

## Prompt Examples

Below are natural language queries you can type to Copilot (or any MCP-aware client) that are likely to trigger the registered tool / prompt:

Plain tool activation examples:

1. "Use the minimal-mcp-server to say hello to Andrei."
2. "Call the say_hello tool with name = Marina."
3. "Ask the MCP server to greet our guest Ivana."

Prompt template usage examples:

1. "Generate the hello_prompt for name=Team."
2. "Get the polite greeting prompt for Ana using hello_prompt."

Chained example (prompt then LLM):

1. "Get the hello_prompt for 'New Contributors' and then draft a welcome message based on it."

Resource fetch examples:

1. "Fetch resource hello://Milan"
2. "Load the greeting resource for Sara (hello://Sara)."

If the client UI allows explicit tool selection, choose `say_hello` and provide JSON args:

```json
{ "name": "Andrei" }
```


## Developer Onboarding (Detailed)

1. Clone repo & enter directory:

```powershell
git clone <REPO_URL> minimal-mcp-server
cd minimal-mcp-server
```

1. Install `uv` (skip if present):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

1. Create venv:

```powershell
uv venv
```

1. Install project deps:

```powershell
uv pip install -e .
```

1. (Optional) Activate venv for ad‑hoc Python:

```powershell
. .\.venv\Scripts\Activate.ps1
```

1. Run server:

```powershell
uv run mcp run server.py
```
1. Open VS Code → Copilot → Configure Tools (server should appear).
1. Invoke `say_hello` tool.

## Verification

```powershell
uv run python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP import OK')"
uv run mcp --help
uv run mcp list-tools server.py   # if supported by your mcp version
```

If `mcp` only works with `uv run`, that's expected (env isolation).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Timeout waiting for initialize | Ensure command is `uv run mcp run server.py` |
| "typer is required" | Reinstall: `uv pip install "mcp[cli]>=1.2.0"` |
| ImportError FastMCP | Reinstall editable: `uv pip install -e .` |

## Common Errors

### ModuleNotFoundError: No module named 'mcp'

Causes:

* Used system Python instead of project environment
* Skipped editable install
* Recreated venv after install (wiped packages)

Fix:

```powershell
uv venv
uv pip install -e .
uv run python -c "import mcp, sys; print('mcp version', mcp.__version__)"
```

Or explicitly:

```powershell
. .\.venv\Scripts\Activate.ps1
python -c "from mcp.server.fastmcp import FastMCP; print('FastMCP OK')"
```

### Server never responds to initialize

* Avoid printing to stdout before protocol starts
* No color wrappers / extraneous logging to stdout
* Debug:

```powershell
uv run mcp run server.py --log-level debug
```

## Adding a New Tool

In `server.py`:

```python
@mcp.tool()
def ping() -> str:
     return "pong"
```

Restart in Copilot → Configure Tools.

## Updating Dependencies

Modify `pyproject.toml`, then:

```powershell
uv pip install -e .
```

Upgrade (respect constraints):

```powershell
uv pip install --upgrade --refresh -e .
```

## Clean Reset

```powershell
Remove-Item -Recurse -Force .venv
uv venv
uv pip install -e .
```

## Recommended Conventions

* Use `uv run` for repeatable execution
* Keep stdout for protocol; send debug to stderr
* Pin only direct deps in `pyproject.toml`

## License

Community internal prototype (free to adapt / extend).
