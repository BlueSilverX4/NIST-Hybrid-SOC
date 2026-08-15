"""Base class for all Battle Chips (IR Playbooks)"""
from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] MMBN-IR :: %(message)s")

class BaseBattleChip(ABC):
    def __init__(self, name: str, code: str, chip_type: str):
        self.name = name          # e.g., "AirGap.EXE"
        self.code = code          # e.g., "A", "B", "*" (Battle Network Chip Codes)
        self.chip_type = chip_type  # Defensive, Offensive, Forensic

    @abstractmethod
    def execute(self, target: str, **kwargs) -> bool:
        """Executes the incident response playbook logic against a target."""
        pass
