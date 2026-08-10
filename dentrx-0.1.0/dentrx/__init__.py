"""DentRx — an open, guideline-cited dental prescribing reference (antibiotics & analgesics).

Educational clinical reference only — NOT a prescription and NOT a substitute for
professional judgement or current official guidelines. See LICENSE and docs/EVIDENCE.md.
"""

from .core import (
    recommend,
    load_rules,
    load_sources,
    pillars,
    DISCLAIMER,
    __version__,
)

__all__ = [
    "recommend",
    "load_rules",
    "load_sources",
    "pillars",
    "DISCLAIMER",
    "__version__",
]
