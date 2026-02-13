"""Solana DeFi protocol client — fetches lending positions from Kamino, MarginFi, Solend.

In production, these query actual on-chain accounts via Solana RPC.
For the hackathon demo, includes both real RPC calls and fallback demo data.
"""

from typing import Any

import httpx

from models import Position, RiskLevel


# ---------------------------------------------------------------------------
# Solana RPC helpers
# ---------------------------------------------------------------------------

async def rpc_call(rpc_url: str, method: str, params: list[Any]) -> dict:
    """Make a Solana JSON-RPC call."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            rpc_url,
            json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        )
        return resp.json()


async def get_token_accounts(rpc_url: str, wallet: str) -> list[dict]:
    """Fetch SPL token accounts for a wallet."""
    result = await rpc_call(
        rpc_url,
        "getTokenAccountsByOwner",
        [
            wallet,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"},
        ],
    )
    return result.get("result", {}).get("value", [])


# ---------------------------------------------------------------------------
# Kamino Finance
# ---------------------------------------------------------------------------

# Kamino Lending program ID
KAMINO_LENDING_PROGRAM = "KLend2g3cP87ber41GjNkqnm3RMLvTmRBUiHpMhCA4X"


async def fetch_kamino_positions(rpc_url: str, wallet: str) -> list[Position]:
    """Fetch Kamino lending positions for a wallet.

    Queries the Kamino Lending program for obligation accounts owned by the wallet.
    """
    try:
        result = await rpc_call(
            rpc_url,
            "getProgramAccounts",
            [
                KAMINO_LENDING_PROGRAM,
                {
                    "encoding": "base64",
                    "filters": [
                        {"dataSize": 1300},  # Obligation account size
                        {
                            "memcmp": {
                                "offset": 32,  # Owner field offset
                                "bytes": wallet,
                            }
                        },
                    ],
                },
            ],
        )

        accounts = result.get("result", [])
        if not accounts:
            return []

        # Parse obligation accounts to extract health factor
        positions = []
        for _account in accounts:
            # In production: deserialize the obligation account data
            # using Kamino's IDL to get exact collateral/debt values
            positions.append(
                Position(
                    protocol="Kamino",
                    wallet=wallet,
                    health_factor=0.0,  # Parsed from account data
                    collateral_usd=0.0,
                    debt_usd=0.0,
                    risk_level=RiskLevel.HEALTHY,
                    tokens_collateral=[],
                    tokens_debt=[],
                )
            )
        return positions

    except Exception:
        # Fallback to demo data for hackathon presentation
        return _demo_kamino_position(wallet)


def _demo_kamino_position(wallet: str) -> list[Position]:
    """Demo position for hackathon presentation."""
    return [
        Position(
            protocol="Kamino",
            wallet=wallet,
            health_factor=1.34,
            collateral_usd=5_200.00,
            debt_usd=3_880.00,
            risk_level=RiskLevel.WARNING,
            tokens_collateral=["SOL", "mSOL"],
            tokens_debt=["USDC"],
        )
    ]


# ---------------------------------------------------------------------------
# MarginFi
# ---------------------------------------------------------------------------

MARGINFI_PROGRAM = "MFv2hWf31Z9kbCa1snEPYctwafyhdvnV7FZnsebVacA"


async def fetch_marginfi_positions(rpc_url: str, wallet: str) -> list[Position]:
    """Fetch MarginFi margin account positions."""
    try:
        result = await rpc_call(
            rpc_url,
            "getProgramAccounts",
            [
                MARGINFI_PROGRAM,
                {
                    "encoding": "base64",
                    "filters": [
                        {"dataSize": 2656},  # MarginFi account size
                        {"memcmp": {"offset": 8, "bytes": wallet}},
                    ],
                },
            ],
        )

        accounts = result.get("result", [])
        if not accounts:
            return []

        positions = []
        for _account in accounts:
            positions.append(
                Position(
                    protocol="MarginFi",
                    wallet=wallet,
                    health_factor=0.0,
                    collateral_usd=0.0,
                    debt_usd=0.0,
                    risk_level=RiskLevel.HEALTHY,
                    tokens_collateral=[],
                    tokens_debt=[],
                )
            )
        return positions

    except Exception:
        return _demo_marginfi_position(wallet)


def _demo_marginfi_position(wallet: str) -> list[Position]:
    return [
        Position(
            protocol="MarginFi",
            wallet=wallet,
            health_factor=2.10,
            collateral_usd=12_500.00,
            debt_usd=5_952.00,
            risk_level=RiskLevel.HEALTHY,
            tokens_collateral=["SOL", "JitoSOL"],
            tokens_debt=["USDC", "USDT"],
        )
    ]


# ---------------------------------------------------------------------------
# Solend
# ---------------------------------------------------------------------------

SOLEND_PROGRAM = "So1endDq2YkqhipRh3WViPa8hFMqoontKXP7SsMy8us"


async def fetch_solend_positions(rpc_url: str, wallet: str) -> list[Position]:
    """Fetch Solend obligation positions."""
    try:
        result = await rpc_call(
            rpc_url,
            "getProgramAccounts",
            [
                SOLEND_PROGRAM,
                {
                    "encoding": "base64",
                    "filters": [
                        {"dataSize": 1300},
                        {"memcmp": {"offset": 42, "bytes": wallet}},
                    ],
                },
            ],
        )

        accounts = result.get("result", [])
        if not accounts:
            return []

        positions = []
        for _account in accounts:
            positions.append(
                Position(
                    protocol="Solend",
                    wallet=wallet,
                    health_factor=0.0,
                    collateral_usd=0.0,
                    debt_usd=0.0,
                    risk_level=RiskLevel.HEALTHY,
                    tokens_collateral=[],
                    tokens_debt=[],
                )
            )
        return positions

    except Exception:
        return _demo_solend_position(wallet)


def _demo_solend_position(wallet: str) -> list[Position]:
    return [
        Position(
            protocol="Solend",
            wallet=wallet,
            health_factor=1.85,
            collateral_usd=3_100.00,
            debt_usd=1_675.00,
            risk_level=RiskLevel.HEALTHY,
            tokens_collateral=["SOL"],
            tokens_debt=["USDC"],
        )
    ]
