# 🛡️ SolShield MCP Server — DeFi Position Monitoring for Kilo Code

> **DeveloperWeek 2026 Hackathon** | Kilo "For Devs, By Devs" Challenge

An open-source **Model Context Protocol (MCP) server** that brings real-time DeFi lending position monitoring directly into your IDE via Kilo Code. Monitor health factors, get liquidation risk alerts, and execute protective rebalances — all without leaving VS Code.

## 🎯 Problem

DeFi developers and power users manage lending positions across Solana protocols (Kamino, MarginFi, Solend) but must constantly context-switch between their IDE and multiple DeFi dashboards. Positions can approach liquidation while developers are deep in a coding session.

## 💡 Solution

**SolShield MCP Server** exposes DeFi monitoring tools via the Model Context Protocol, allowing Kilo Code to natively query and act on lending positions:

```
Developer in VS Code → Kilo Code → SolShield MCP Server → Solana DeFi Protocols
```

### MCP Tools Exposed

| Tool | Description |
|------|-------------|
| `check_health_factor` | Query health factor for any wallet across Kamino/MarginFi/Solend |
| `get_position_risk` | AI-powered risk assessment with Claude analysis |
| `list_positions` | List all lending positions for a wallet |
| `simulate_rebalance` | Simulate a rebalancing strategy before execution |
| `execute_rebalance` | Execute protective rebalance via Jupiter swaps |
| `set_alert_threshold` | Configure health factor alert thresholds |

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  VS Code / JetBrains IDE                                     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Kilo Code (AI Coding Agent)                           │  │
│  │  "Check my DeFi positions" → MCP Tool Call             │  │
│  └────────────────────┬───────────────────────────────────┘  │
└───────────────────────┼──────────────────────────────────────┘
                        │ MCP Protocol (stdio/SSE)
┌───────────────────────┼──────────────────────────────────────┐
│  SolShield MCP Server │                                      │
│  ┌────────────┐  ┌────┴───────┐  ┌────────────┐             │
│  │ Position   │  │ Claude AI  │  │ Jupiter    │             │
│  │ Monitor    │  │ Analyzer   │  │ Executor   │             │
│  └─────┬──────┘  └────────────┘  └─────┬──────┘             │
└────────┼────────────────────────────────┼────────────────────┘
         │ Solana RPC (Helius)            │ Jupiter API
┌────────┼────────────────────────────────┼────────────────────┐
│  Solana│Blockchain                      │                    │
│  ┌─────┴──────┐  ┌───────────┐  ┌──────┴─────┐             │
│  │ Kamino     │  │ MarginFi  │  │ Jupiter    │             │
│  │ Solend     │  │           │  │ Aggregator │             │
│  └────────────┘  └───────────┘  └────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Kilo Code (VS Code or JetBrains)
- Solana RPC endpoint (Helius recommended)

### Install

```bash
git clone https://github.com/mgnlia/devweek-2026-submission.git
cd devweek-2026-submission
uv sync
```

### Configure

```bash
cp .env.example .env
# Add your keys:
# HELIUS_API_KEY=your_key
# ANTHROPIC_API_KEY=your_key
```

### Add to Kilo Code

Add to your Kilo MCP settings (`.kilo/mcp.json`):

```json
{
  "mcpServers": {
    "solshield": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/devweek-2026-submission"
    }
  }
}
```

### Use in Kilo

```
You: "Check the health factor for wallet 7xKXtg..."
Kilo: [Calls check_health_factor] → "Kamino position: HF 1.34 (WARNING)
      MarginFi position: HF 2.1 (HEALTHY). Recommend adding $200 
      collateral to Kamino position to bring HF above 1.5."
```

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| MCP Server | Python 3.11, `mcp` SDK |
| AI Analysis | Anthropic Claude API |
| Blockchain | Solana, solders, solana-py |
| DeFi Protocols | Kamino, MarginFi, Solend |
| Swap Routing | Jupiter Aggregator v6 |
| Package Manager | uv |

## 🏆 Judging Criteria Alignment

| Criteria | How We Deliver |
|----------|---------------|
| **Utility** | Real problem: devs lose funds to liquidation while coding. MCP integration = zero context-switch monitoring |
| **Code Quality** | Typed Python, structured logging, comprehensive error handling, MCP SDK best practices |
| **"Would we use this?"** | Any DeFi developer using Kilo Code gets free liquidation protection in their IDE |

## 📊 Key Features

- **Multi-Protocol**: Monitors Kamino, MarginFi, and Solend simultaneously
- **AI-Powered Analysis**: Claude evaluates risk with market context, not just thresholds
- **MCP Native**: Built on the Model Context Protocol standard — works with any MCP-compatible client
- **Open Source**: MIT licensed, designed for community contribution
- **Autonomous Alerts**: Proactive notifications when positions approach danger zones

## 🔗 Links

- **Demo**: [Live Dashboard](https://solshield-devweek.vercel.app)
- **Backend Agent**: [colosseum-agent-hackathon](https://github.com/mgnlia/colosseum-agent-hackathon)
- **Frontend**: [liquidation-agent-frontend](https://github.com/mgnlia/liquidation-agent-frontend)

## 📄 License

MIT

## 🤖 Built With

Built by an AI-powered development team using Claude (Anthropic) for both code generation and runtime DeFi analysis. Submitted to DeveloperWeek 2026 Hackathon — Kilo "For Devs, By Devs" Challenge.
