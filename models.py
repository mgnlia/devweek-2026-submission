"""Domain types for SolShield MCP Server.

Shared between server.py and solana_client.py to avoid circular imports.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


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
