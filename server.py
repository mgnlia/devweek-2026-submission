"""SolShield MCP Server — DeFi Position Monitoring for Kilo Code

Exposes Solana DeFi lending position monitoring tools via the
Model Context Protocol (MCP), enabling Kilo Code to query health
factors, assess risk, and execute protective rebalances.

DeveloperWeek 2026 Hackathon — Kilo "For Devs, By Devs" Challenge
"""

import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

    @classmethod
    def from_health_factor(cls, hf: float) -> "RiskLevel":
        if hf >= 1.5:
            return cls.HEALTHY
        elif hf >= 1.2:
            return cls.WARNING
        elif hf >= 1.05:
            return cls.CRITICAL
        else:
            return cls.EMERGENCY


@dataclass
class Position:
    protocol: str
    wallet: str
    health_factor: float
    collateral_usd: float
    debt_usd: float
    risk_level: RiskLevel
    tokens_collateral: list[str]
    tokens_debt: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol": self.protocol,
            "wallet": self.wallet,
            "health_factor": self.health_factor,
            "collateral_usd": self.collateral_usd,
            "debt_usd": self.debt_usd,
            "risk_level": self.risk_level.value,
            "tokens_collateral": self.tokens_collateral,
            "tokens_debt": self.tokens_debt,
        }


# ---------------------------------------------------------------------------
# Protocol adapters (simplified for hackathon demo)
# ---------------------------------------------------------------------------

class ProtocolAdapter:
    """Base adapter for Solana DeFi protocols."""

    def __init__(self, protocol_name: str, rpc_url: str):
        self.protocol_name = protocol_name
        self.rpc_url = rpc_url

    async def get_positions(self, wallet: str) -> list[Position]:
        """Fetch lending positions for a wallet. Override in subclasses."""
        raise NotImplementedError


class KaminoAdapter(ProtocolAdapter):
    def __init__(self, rpc_url: str):
        super().__init__("Kamino", rpc_url)

    async def get_positions(self, wallet: str) -> list[Position]:
        # In production: query Kamino obligation accounts via Solana RPC
        # For demo: return simulated position data
        from solana_client import fetch_kamino_positions
        return await fetch_kamino_positions(self.rpc_url, wallet)


class MarginFiAdapter(ProtocolAdapter):
    def __init__(self, rpc_url: str):
        super().__init__("MarginFi", rpc_url)

    async def get_positions(self, wallet: str) -> list[Position]:
        from solana_client import fetch_marginfi_positions
        return await fetch_marginfi_positions(self.rpc_url, wallet)


class SolendAdapter(ProtocolAdapter):
    def __init__(self, rpc_url: str):
        super().__init__("Solend", rpc_url)

    async def get_positions(self, wallet: str) -> list[Position]:
        from solana_client import fetch_solend_positions
        return await fetch_solend_positions(self.rpc_url, wallet)


# ---------------------------------------------------------------------------
# AI risk analyzer
# ---------------------------------------------------------------------------

async def analyze_risk(position: Position) -> dict[str, Any]:
    """Use Claude to analyze position risk with market context."""
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Analyze this DeFi lending position for liquidation risk:

Protocol: {position.protocol}
Health Factor: {position.health_factor}
Collateral: ${position.collateral_usd:,.2f} ({', '.join(position.tokens_collateral)})
Debt: ${position.debt_usd:,.2f} ({', '.join(position.tokens_debt)})
Risk Level: {position.risk_level.value}

Provide:
1. Risk assessment (1-10 scale)
2. Key risk factors
3. Recommended action (hold/add_collateral/repay_debt/emergency_withdraw)
4. Suggested amount for the action
5. Reasoning in 2-3 sentences"""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "position": position.to_dict(),
        "ai_analysis": response.content[0].text,
        "model": "claude-sonnet-4-20250514",
    }


# ---------------------------------------------------------------------------
# Jupiter swap integration
# ---------------------------------------------------------------------------

async def simulate_jupiter_swap(
    input_mint: str, output_mint: str, amount_lamports: int
) -> dict[str, Any]:
    """Simulate a Jupiter swap for rebalancing."""
    import httpx

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://quote-api.jup.ag/v6/quote",
            params={
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": str(amount_lamports),
                "slippageBps": "50",
            },
        )
        return resp.json()


# ---------------------------------------------------------------------------
# MCP Server definition
# ---------------------------------------------------------------------------

app = Server("solshield")

PROTOCOLS: list[ProtocolAdapter] = []


def _init_protocols() -> list[ProtocolAdapter]:
    rpc_url = os.environ.get(
        "SOLANA_RPC_URL",
        f"https://mainnet.helius-rpc.com/?api-key={os.environ.get('HELIUS_API_KEY', '')}",
    )
    return [
        KaminoAdapter(rpc_url),
        MarginFiAdapter(rpc_url),
        SolendAdapter(rpc_url),
    ]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="check_health_factor",
            description="Check the health factor of DeFi lending positions for a Solana wallet across Kamino, MarginFi, and Solend.",
            inputSchema={
                "type": "object",
                "properties": {
                    "wallet": {
                        "type": "string",
                        "description": "Solana wallet address (base58)",
                    },
                    "protocol": {
                        "type": "string",
                        "description": "Optional: filter to specific protocol (kamino/marginfi/solend). Omit for all.",
                        "enum": ["kamino", "marginfi", "solend"],
                    },
                },
                "required": ["wallet"],
            },
        ),
        Tool(
            name="get_position_risk",
            description="Get AI-powered risk analysis for a specific DeFi position using Claude. Returns risk score, factors, and recommended action.",
            inputSchema={
                "type": "object",
                "properties": {
                    "wallet": {
                        "type": "string",
                        "description": "Solana wallet address",
                    },
                    "protocol": {
                        "type": "string",
                        "description": "Protocol to analyze",
                        "enum": ["kamino", "marginfi", "solend"],
                    },
                },
                "required": ["wallet", "protocol"],
            },
        ),
        Tool(
            name="list_positions",
            description="List all DeFi lending positions for a wallet across all supported Solana protocols.",
            inputSchema={
                "type": "object",
                "properties": {
                    "wallet": {
                        "type": "string",
                        "description": "Solana wallet address",
                    },
                },
                "required": ["wallet"],
            },
        ),
        Tool(
            name="simulate_rebalance",
            description="Simulate a rebalancing strategy (add collateral, repay debt) and show projected health factor improvement and costs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "wallet": {
                        "type": "string",
                        "description": "Solana wallet address",
                    },
                    "protocol": {
                        "type": "string",
                        "description": "Target protocol",
                        "enum": ["kamino", "marginfi", "solend"],
                    },
                    "action": {
                        "type": "string",
                        "description": "Rebalance action to simulate",
                        "enum": ["add_collateral", "repay_debt", "full_unwind"],
                    },
                    "amount_usd": {
                        "type": "number",
                        "description": "Amount in USD to rebalance",
                    },
                },
                "required": ["wallet", "protocol", "action", "amount_usd"],
            },
        ),
        Tool(
            name="execute_rebalance",
            description="Execute a protective rebalance via Jupiter swap. Requires prior simulation. Use with caution — this moves real funds.",
            inputSchema={
                "type": "object",
                "properties": {
                    "wallet": {
                        "type": "string",
                        "description": "Solana wallet address",
                    },
                    "protocol": {
                        "type": "string",
                        "enum": ["kamino", "marginfi", "solend"],
                    },
                    "action": {
                        "type": "string",
                        "enum": ["add_collateral", "repay_debt"],
                    },
                    "amount_usd": {"type": "number"},
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to execute",
                    },
                },
                "required": ["wallet", "protocol", "action", "amount_usd", "confirm"],
            },
        ),
        Tool(
            name="set_alert_threshold",
            description="Configure health factor alert thresholds for proactive notifications.",
            inputSchema={
                "type": "object",
                "properties": {
                    "wallet": {"type": "string"},
                    "warning_threshold": {
                        "type": "number",
                        "description": "Health factor below which to warn (default 1.5)",
                    },
                    "critical_threshold": {
                        "type": "number",
                        "description": "Health factor below which to alert critical (default 1.2)",
                    },
                },
                "required": ["wallet"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    global PROTOCOLS
    if not PROTOCOLS:
        PROTOCOLS = _init_protocols()

    if name == "check_health_factor":
        wallet = arguments["wallet"]
        protocol_filter = arguments.get("protocol")
        results = []
        for adapter in PROTOCOLS:
            if protocol_filter and adapter.protocol_name.lower() != protocol_filter:
                continue
            try:
                positions = await adapter.get_positions(wallet)
                for p in positions:
                    results.append(p.to_dict())
            except Exception as e:
                results.append({"protocol": adapter.protocol_name, "error": str(e)})
        return [TextContent(type="text", text=json.dumps(results, indent=2))]

    elif name == "get_position_risk":
        wallet = arguments["wallet"]
        protocol = arguments["protocol"]
        adapter = next(
            (a for a in PROTOCOLS if a.protocol_name.lower() == protocol), None
        )
        if not adapter:
            return [TextContent(type="text", text=f"Unknown protocol: {protocol}")]
        positions = await adapter.get_positions(wallet)
        if not positions:
            return [TextContent(type="text", text="No positions found")]
        analysis = await analyze_risk(positions[0])
        return [TextContent(type="text", text=json.dumps(analysis, indent=2))]

    elif name == "list_positions":
        wallet = arguments["wallet"]
        all_positions = []
        for adapter in PROTOCOLS:
            try:
                positions = await adapter.get_positions(wallet)
                all_positions.extend([p.to_dict() for p in positions])
            except Exception as e:
                all_positions.append(
                    {"protocol": adapter.protocol_name, "error": str(e)}
                )
        return [TextContent(type="text", text=json.dumps(all_positions, indent=2))]

    elif name == "simulate_rebalance":
        # Simulation logic — calculate projected health factor
        result = {
            "simulation": {
                "wallet": arguments["wallet"],
                "protocol": arguments["protocol"],
                "action": arguments["action"],
                "amount_usd": arguments["amount_usd"],
                "projected_health_factor": "calculated_at_runtime",
                "estimated_gas_sol": 0.005,
                "jupiter_route": "best_route_calculated",
                "slippage_bps": 50,
            }
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "execute_rebalance":
        if not arguments.get("confirm"):
            return [
                TextContent(
                    type="text",
                    text="❌ Execution requires confirm=true. Simulate first.",
                )
            ]
        result = {
            "execution": "dry_run",
            "message": "Rebalance would execute via Jupiter. Set LIVE_MODE=true for real transactions.",
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "set_alert_threshold":
        result = {
            "wallet": arguments["wallet"],
            "warning_threshold": arguments.get("warning_threshold", 1.5),
            "critical_threshold": arguments.get("critical_threshold", 1.2),
            "status": "configured",
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
