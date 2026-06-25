# mvqueen_engine/engine_state.py

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Literal
import time
import uuid


class EnginePhase(Enum):
    """High-level lifecycle phases for the MVQueen engine."""
    INIT = auto()
    LOADING_CONFIG = auto()
    LOADING_BANKS = auto()
    DETECTING = auto()
    EDITORIAL = auto()
    SYNCING = auto()
    IDLE = auto()
    ERROR = auto()
    SHUTDOWN = auto()


class EngineMode(Enum):
    """Operating modes for the engine."""
    OFFLINE = auto()
    ONLINE = auto()
    DRY_RUN = auto()
    TEST = auto()


@dataclass
class RunContext:
    """Context for a single run/batch."""
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    batch_id: Optional[str] = None
    source: Literal["csv", "api", "manual"] = "csv"
    shop_name: Optional[str] = None
    started_at: float = field(default_factory=time.time)
    finished_at: Optional[float] = None

    def mark_finished(self) -> None:
        self.finished_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EngineConfigSnapshot:
    """Snapshot of the active config/control panel at runtime."""
    profile: Optional[str] = None
    persona: Optional[str] = None
    locale: str = "en"
    currency: str = "USD"
    channel: Literal["shopify", "preview", "export"] = "shopify"
    toggles: Dict[str, bool] = field(default_factory=dict)
    raw_config: Dict[str, Any] = field(default_factory=dict)

    def is_enabled(self, key: str, default: bool = True) -> bool:
        return self.toggles.get(key, default)


@dataclass
class EngineDiagnostics:
    """Lightweight diagnostics and counters for observability."""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    processed_products: int = 0
    skipped_products: int = 0
    successful_uploads: int = 0
    failed_uploads: int = 0

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EngineState:
    """
    Single source of truth for the engine's runtime state.

    This is what the engine reads/writes as it moves through:
    - config loading
    - brand banks loading
    - detection
    - editorial
    - sync (Shopify, etc.)
    """
    phase: EnginePhase = EnginePhase.INIT
    mode: EngineMode = EngineMode.OFFLINE
    is_ready: bool = False
    has_fatal_error: bool = False

    run_context: RunContext = field(default_factory=RunContext)
    config_snapshot: EngineConfigSnapshot = field(default_factory=EngineConfigSnapshot)
    diagnostics: EngineDiagnostics = field(default_factory=EngineDiagnostics)

    # Arbitrary scratchpad for modules to stash data
    scratch: Dict[str, Any] = field(default_factory=dict)

    def set_phase(self, phase: EnginePhase) -> None:
        self.phase = phase

    def set_mode(self, mode: EngineMode) -> None:
        self.mode = mode

    def mark_ready(self) -> None:
        self.is_ready = True
        self.has_fatal_error = False

    def mark_error(self, message: str, fatal: bool = True) -> None:
        self.diagnostics.add_error(message)
        if fatal:
            self.has_fatal_error = True
            self.phase = EnginePhase.ERROR

    def attach_config(self, profile: str, persona: str,
                      toggles: Dict[str, bool],
                      raw_config: Dict[str, Any],
                      locale: str = "en",
                      currency: str = "USD",
                      channel: Literal["shopify", "preview", "export"] = "shopify") -> None:
        self.config_snapshot = EngineConfigSnapshot(
            profile=profile,
            persona=persona,
            locale=locale,
            currency=currency,
            channel=channel,
            toggles=toggles,
            raw_config=raw_config,
        )

    def bump_processed(self, count: int = 1) -> None:
        self.diagnostics.processed_products += count

    def bump_skipped(self, count: int = 1) -> None:
        self.diagnostics.skipped_products += count

    def bump_upload_success(self, count: int = 1) -> None:
        self.diagnostics.successful_uploads += count

    def bump_upload_failed(self, count: int = 1) -> None:
        self.diagnostics.failed_uploads += count

    def set_scratch(self, key: str, value: Any) -> None:
        self.scratch[key] = value

    def get_scratch(self, key: str, default: Any = None) -> Any:
        return self.scratch.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase.name,
            "mode": self.mode.name,
            "is_ready": self.is_ready,
            "has_fatal_error": self.has_fatal_error,
            "run_context": self.run_context.to_dict(),
            "config_snapshot": asdict(self.config_snapshot),
            "diagnostics": self.diagnostics.to_dict(),
            "scratch": self.scratch,
        }
# ------------------------------------------------------------
# GLOBAL ENGINE STATE SINGLETON
# ------------------------------------------------------------

_engine_state = EngineState()


def get_engine_state() -> EngineState:
    return _engine_state