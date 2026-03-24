from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field
from time import perf_counter


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


logger = logging.getLogger("atlas_rag")


@dataclass
class MetricsRegistry:
    counters: Counter[str] = field(default_factory=Counter)
    latency_samples: list[float] = field(default_factory=list)

    def increment(self, key: str, count: int = 1) -> None:
        self.counters[key] += count

    def observe(self, latency_seconds: float) -> None:
        self.latency_samples.append(latency_seconds)

    def render_prometheus(self) -> str:
        avg = sum(self.latency_samples) / len(self.latency_samples) if self.latency_samples else 0.0
        lines = [
            "# HELP atlas_requests_total Total request count",
            "# TYPE atlas_requests_total counter",
        ]
        lines.extend(f'atlas_requests_total{{type="{key}"}} {value}' for key, value in sorted(self.counters.items()))
        lines.extend(
            [
                "# HELP atlas_request_latency_seconds_avg Average request latency",
                "# TYPE atlas_request_latency_seconds_avg gauge",
                f"atlas_request_latency_seconds_avg {avg:.6f}",
            ]
        )
        return "\n".join(lines) + "\n"


metrics = MetricsRegistry()


class RequestTimer:
    def __enter__(self) -> "RequestTimer":
        self.started_at = perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        metrics.observe(perf_counter() - self.started_at)

