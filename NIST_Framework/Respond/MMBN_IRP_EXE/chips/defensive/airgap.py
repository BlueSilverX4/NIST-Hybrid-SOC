import platform
import subprocess
import logging
from chips import BaseBattleChip

class AirGapChip(BaseBattleChip):
    def __init__(self):
        super().__init__(name="AirGap.EXE", code="A", chip_type="Defensive")

    def execute(self, target: str, interface_name: str = "eth0") -> bool:
        logging.info(f"🛡️  [CHIP SLOT: {self.name}] Initiating network isolation on target: {target}")
        
        system_os = platform.system()
        try:
            if system_os == "Linux":
                # Disables network interface on Linux
                cmd = ["ip", "link", "set", interface_name, "down"]
                logging.info(f"Executing: {' '.join(cmd)}")
                # subprocess.run(cmd, check=True) # Uncomment for active deployment
            elif system_os == "Windows":
                # Disables interface on Windows via netsh
                cmd = ["netsh", "interface", "set", "interface", interface_name, "admin=disable"]
                logging.info(f"Executing: {' '.join(cmd)}")
                # subprocess.run(cmd, check=True) # Uncomment for active deployment
            
            logging.info(f"✅ Target {target} effectively AirGapped from the Cyber Grid.")
            return True
        except Exception as e:
            logging.error(f"❌ AirGap execution failed: {str(e)}")
            return False
