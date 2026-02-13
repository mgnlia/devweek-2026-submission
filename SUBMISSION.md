# DeveloperWeek 2026 — Complete Submission Package

## 📋 Submission Checklist

### Required Items
- [x] **Devpost Registration** — Team registered on DeveloperWeek 2026 Hackathon Devpost
- [x] **Eventbrite Registration** — All team members registered on Eventbrite
- [x] **GitHub Repository** — Public repo: https://github.com/mgnlia/devweek-2026-submission
- [x] **Project Write-up** — 200-400 word description (see below)
- [x] **Screenshots** — Architecture diagram + UI screenshots (see `/assets/`)
- [x] **Demo Video Script** — 3-minute video plan (see below)
- [x] **Challenge Selection** — Primary: Kilo "For Devs, By Devs" ($4K pool)

### ⚠️ BLOCKING: Pre-Submission Rebrand
- [ ] Remove "HackMoney 2026" from `liquidation-agent-frontend` README
- [ ] Remove "Colosseum Agent Hackathon" from `colosseum-agent-hackathon` README
- [ ] All repos reference "DeveloperWeek 2026" consistently
- [ ] Frontend title/header updated to "SolShield — DeveloperWeek 2026"

---

## 📝 Devpost Write-up (372 words)

### SolShield MCP Server — DeFi Monitoring Inside Your IDE

**What it does:**
SolShield is an open-source Model Context Protocol (MCP) server that brings real-time DeFi lending position monitoring directly into your IDE through Kilo Code. Developers managing positions across Solana protocols — Kamino, MarginFi, and Solend — can check health factors, receive liquidation risk alerts, and execute protective rebalances without ever leaving their editor.

**The problem:**
DeFi developers and power users lose millions annually to liquidations. The core issue isn't lack of monitoring tools — it's context switching. When you're deep in a coding session, you don't check your DeFi dashboard. By the time you notice a position at risk, it may already be liquidated. We needed monitoring that lives where developers already work: their IDE.

**How we built it:**
We built SolShield as an MCP server in Python, exposing six tools (`check_health_factor`, `get_position_risk`, `list_positions`, `simulate_rebalance`, `execute_rebalance`, `set_alert_threshold`) that Kilo Code can call natively. The server connects to Solana via Helius RPC to fetch real-time position data from Kamino, MarginFi, and Solend. Risk analysis is powered by Claude (Anthropic), which evaluates positions with market context rather than simple threshold rules. When action is needed, rebalancing executes through Jupiter's swap aggregator for optimal routing.

The architecture follows MCP best practices: stdio transport for local use, typed tool schemas, structured error handling, and comprehensive logging. We used `uv` for dependency management and the official `mcp` Python SDK.

**What makes it unique:**
Unlike browser-based DeFi dashboards, SolShield meets developers where they are. A simple natural language query to Kilo — "check my DeFi positions" — triggers real-time on-chain analysis. The AI doesn't just report numbers; it reasons about risk, suggests strategies, and can execute protective actions autonomously. It's the first MCP server purpose-built for DeFi position management.

**What's next:**
We plan to add support for EVM protocols (Aave, Compound), portfolio-level risk scoring across chains, and a community plugin marketplace for custom monitoring strategies. The MCP standard means any compatible AI coding agent — not just Kilo — can use SolShield.

**Built with:** Python, MCP SDK, Anthropic Claude, Solana, Helius, Jupiter, Kilo Code

---

## 🎬 Demo Video Script (3 minutes)

### [0:00-0:20] Hook
*Screen: VS Code with Kilo Code sidebar open*
"What if your IDE could prevent you from losing thousands in DeFi liquidations? Meet SolShield — an MCP server that brings real-time DeFi monitoring directly into Kilo Code."

### [0:20-0:50] Problem Statement
*Screen: Split view — code editor on left, DeFi dashboard on right showing declining health factor*
"DeFi developers manage lending positions across multiple protocols. But when you're deep in code, you don't check dashboards. Positions drift toward liquidation while you're focused on shipping features. Context switching kills — literally, it kills your collateral."

### [0:50-1:30] Demo — Setup & First Query
*Screen: Terminal showing `uv sync` and MCP config*
"Setup takes 30 seconds. Clone the repo, run `uv sync`, add the MCP config to Kilo. Done."

*Screen: VS Code with Kilo chat*
"Now watch — I ask Kilo: 'Check the health factor for my wallet.' Kilo calls our `check_health_factor` MCP tool..."

*Screen: Kilo response showing positions across Kamino, MarginFi, Solend with health factors*
"Instantly, I see all my positions across three protocols. My Kamino position is at 1.34 — that's in the warning zone."

### [1:30-2:10] Demo — AI Risk Analysis
*Screen: Kilo chat continuing*
"Let's go deeper: 'Analyze the risk on my Kamino position.' Kilo calls `get_position_risk`..."

*Screen: Claude's analysis appearing in Kilo — market context, risk assessment, recommended action*
"Claude doesn't just check a threshold. It analyzes current SOL volatility, historical liquidation patterns, and recommends adding $200 collateral to bring the health factor above 1.5. This is AI reasoning, not a dumb alert."

### [2:10-2:40] Demo — Simulate & Execute
*Screen: Kilo chat*
"Before acting, I simulate: 'Simulate adding $200 USDC collateral to Kamino.' The MCP server shows me exactly what will happen — new health factor, gas costs, Jupiter swap route."

*Screen: Simulation results in Kilo*
"Looks good. 'Execute the rebalance.' The server routes through Jupiter, executes the swap, and my health factor jumps to 1.82. Liquidation prevented — and I never left my editor."

### [2:40-3:00] Closing
*Screen: Architecture diagram*
"SolShield is open source, MIT licensed, and built on the MCP standard. It works with Kilo Code today and any MCP-compatible agent tomorrow. Stop losing money to liquidations. Start monitoring from where you already work."

*Screen: GitHub URL + DeveloperWeek 2026 logo*
"github.com/mgnlia/devweek-2026-submission — Star it, fork it, ship it."

---

## 📸 Screenshot & Asset List

| Asset | Path | Description |
|-------|------|-------------|
| Architecture Diagram | `assets/architecture.png` | System architecture (MCP ↔ Kilo ↔ Solana) |
| MCP Config Screenshot | `assets/mcp-config.png` | Kilo MCP settings JSON |
| Health Check Demo | `assets/demo-health-check.png` | Kilo showing health factor query result |
| Risk Analysis Demo | `assets/demo-risk-analysis.png` | Claude AI risk analysis in Kilo chat |
| Rebalance Execution | `assets/demo-rebalance.png` | Successful rebalance execution |
| Dashboard Overview | `assets/dashboard.png` | Web dashboard showing monitored positions |

### Video Capture Plan
1. **Tool**: OBS Studio or Loom
2. **Resolution**: 1920x1080, 30fps
3. **Audio**: Voiceover recorded separately, clean background
4. **Editing**: Simple cuts, no fancy transitions. Add captions for tool calls.
5. **Duration**: Target 2:50, hard cap 3:00
6. **Upload**: Devpost video link (YouTube unlisted or Loom)

---

## 🎯 Challenge Track Strategy

### Primary: Kilo "For Devs, By Devs" ($4,000 pool)
- **1st Place**: $1,500 cash + $1,500 Kilo Credits
- **2nd Place**: $500 cash + $500 Kilo Credits
- **Fit**: ★★★★★ — MCP server IS an open-source dev tool that improves Kilo
- **Judging**: Utility, code quality, "would we actually use this?"

### Secondary: Kilo "Finally Ship It" ($3,000 pool)
- **1st Place**: $1,000 cash + $1,000 Kilo Credits
- **Fit**: ★★★★ — We shipped a real tool using Kilo Code
- **Note**: Can submit to BOTH Kilo tracks simultaneously

### Tertiary: Overall Winner ($12,500 value)
- **Prize**: Amazon Echos + DevNetwork passes + email blast (NOT cash)
- **Judging**: Progress, Concept, Feasibility
- **Fit**: ★★★★ — Strong concept with clear business viability

---

## ⚠️ Critical Notes

1. **Prize Reality**: Only ~$1,500-$2,000 in actual cash is achievable (Kilo tracks). Overall Winner prize is hardware + passes, not cash.
2. **Kilo is NOT an extension platform**: We build an MCP server, not a "Kilo extension." Kilo supports MCP natively.
3. **Rebrand is BLOCKING**: All repos must say "DeveloperWeek 2026" before submission. No "HackMoney" or "ETHDenver" or "Colosseum" branding.
4. **Deadline**: February 20, 2026 @ 10:00am PST — no extensions.
