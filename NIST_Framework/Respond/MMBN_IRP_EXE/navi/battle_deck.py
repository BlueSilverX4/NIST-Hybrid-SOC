from typing import List, Dict, Any
import logging
from chips import BaseBattleChip

class BattleDeck:
    def __init__(self):
        self.active_folder: List[BaseBattleChip] = []

    def load_chip(self, chip: BaseBattleChip):
        if len(self.active_folder) < 5:  # Battle Network 5-chip custom screen limit
            self.active_folder.append(chip)
            logging.info(f"🎴 Slotted Battle Chip: [{chip.name} - Code: {chip.code}]")
        else:
            logging.warning("Folder buffer full! Cannot load more chips this turn.")

    def execute_turn(self, target: str, context: Dict[str, Any]) -> bool:
        logging.info("=== ⚡ JACK IN! EXECUTING BATTLE CHIP COMBO ⚡ ===")
        all_success = True
        
        for chip in self.active_folder:
            # Map context parameters dynamically to chip requirements
            param = context.get(chip.name, {})
            result = chip.execute(target=target, **param)
            if not result:
                all_success = False
                
        self.active_folder.clear() # Reset custom screen folder after turn
        return all_success
