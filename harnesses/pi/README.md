# Pi

## Install

Install Pi and sign in to your model provider. From the EP Agent checkout, run
the universal installer and choose Pi:

```bash
./install.sh
```

The installer launches EDSL's `ep auth login` flow when an Expected Parrot key
is not already configured, prepares the locked Python and EDSL runtime, and
adds EP Agent to Pi. It then offers to sign in to a model provider; you can
also do this later from Pi with `/login`. Start Pi in the project where you
want to work and describe your research task. Rerun the installer after
updating the checkout.

To install a published release directly with Pi:

```bash
pi install git:github.com/expectedparrot/ep-ra@<release-tag>
```

For EDSL commands, activate the checkout's `.venv` in the shell that launches
Pi:

```bash
source /path/to/ep-ra/.venv/bin/activate
```

Pi provider sign-in is managed by Pi, for example `pi auth login anthropic`.

## Optional web extraction

Firecrawl can support bounded extraction from structured web sources. Add its
MCP server to `~/.pi/agent/mcp.json` and provide `FIRECRAWL_API_KEY` through
your environment or secret manager:

```json
{
  "mcpServers": {
    "firecrawl": {
      "url": "https://mcp.firecrawl.dev/${FIRECRAWL_API_KEY}/v2/mcp"
    }
  }
}
```

Keep API keys out of this repository and shared project configuration.
