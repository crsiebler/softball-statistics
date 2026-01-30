"""
Base classes for parsers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class Parser(ABC):
    """Abstract base class for parsers."""

    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse data from file path and return structured result."""
        pass
