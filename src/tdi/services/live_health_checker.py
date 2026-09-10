from datetime import datetime, timezone
from pathlib import Path


class LiveHealthChecker:
    def __init__(self, stale_after_seconds: int):
        self.stale_after_seconds = stale_after_seconds

    def is_healthy(
        self,
        state_file: Path,
        now: datetime | None = None,
    ) -> bool:
        if not state_file.exists():
            return False

        if now is None:
            now = datetime.now(timezone.utc)

        modified_at = datetime.fromtimestamp(
            state_file.stat().st_mtime,
            tz=timezone.utc,
        )

        age_seconds = (now - modified_at).total_seconds()

        return age_seconds <= self.stale_after_seconds

    def requires_recovery(
        self,
        state_files: list[Path],
        now: datetime | None = None,
    ) -> bool:
        return any(
            not self.is_healthy(state_file, now=now)
            for state_file in state_files
        )
    