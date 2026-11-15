# Pi

## Install

Install Pi and sign in to your model provider. From the EP Agent checkout, run
the universal installer and choose Pi:

```bash
./install.sh
```

The installer requires and verifies an Expected Parrot API key, prepares the
locked Python and EDSL runtime, and adds EP Agent to Pi. Start Pi in the project
where you want to work and describe your research task. Rerun the installer
after updating the checkout.

To install a published release directly with Pi:

```bash
pi install git:github.com/expectedparrot/ep-agent@<release-tag>
```

For EDSL commands, activate the checkout's `.venv` in the shell that launches
Pi. The installer prints the activation command. Pi provider sign-in is managed
by Pi, for example `pi auth login anthropic`.

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
