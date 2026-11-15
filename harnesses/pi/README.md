# Pi

## Install

Install Pi and sign in to your model provider. From the EP Agent checkout, run:

```bash
./installers/install-pi.sh
```

The installer adds EP Agent to Pi and prepares the locked Python and EDSL
runtime. Add `--skills-only` to skip the runtime. Start Pi in the project where
you want to work and describe your research task. Rerun the installer after
updating the checkout.

To install a published release directly with Pi:

```bash
pi install git:github.com/expectedparrot/ep-agent@<release-tag>
```

## Expected Parrot access

EDSL-backed research requires an Expected Parrot API key. Export
`EXPECTED_PARROT_API_KEY` before launching Pi, or configure the EDSL CLI from
the checkout:

```bash
uv run --frozen --no-dev ep auth login --api_key <your-key>
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
