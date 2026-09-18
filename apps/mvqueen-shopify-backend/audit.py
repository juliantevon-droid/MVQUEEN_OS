from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any


class AuditLog:
    """Small persistent audit trail for backend actions.

    SQLite is intended for development/staging. Production can replace this
    storage adapter without changing the application-facing interface.
    """

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or Path(__file__).resolve().parent / "runtime" / "audit.sqlite3")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    actor TEXT,
                    shop_domain TEXT,
                    resource_id TEXT,
                    dry_run INTEGER NOT NULL,
                    details_json TEXT NOT NULL
                )
                """
            )

    def record(
        self,
        event_type: str,
        *,
        actor: str | None = None,
        shop_domain: str | None = None,
        resource_id: str | None = None,
        dry_run: bool = True,
        details: dict[str, Any] | None = None,
    ) -> None:
        with self._lock, self._connect() as db:
            db.execute(
                """
                INSERT INTO audit_events
                (created_at, event_type, actor, shop_domain, resource_id, dry_run, details_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    event_type,
                    actor,
                    shop_domain,
                    resource_id,
                    int(dry_run),
                    json.dumps(details or {}, sort_keys=True),
                ),
            )

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 200))
        with self._connect() as db:
            rows = db.execute(
                "SELECT * FROM audit_events ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]


audit_log = AuditLog()
