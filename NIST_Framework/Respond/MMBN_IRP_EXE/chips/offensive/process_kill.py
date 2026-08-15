import os
import signal
import psutil
import logging
from chips import BaseBattleChip

class ProcessKillChip(BaseBattleChip):
    def __init__(self):
        super().__init__(name="ProcessKill.EXE", code="K", chip_type="Offensive")

    def execute(self, target: str, pid: int = None) -> bool:
        if not pid:
            logging.error("❌ ProcessKill requires a target Process ID (PID).")
            return False

        logging.info(f"⚔️  [CHIP SLOT: {self.name}] Target acquired -> PID {pid} on {target}")
        
        try:
            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                proc_name = process.name()
                
                # Terminate child processes first
                for child in process.children(recursive=True):
                    logging.info(f"Busting child process: {child.name()} (PID: {child.pid})")
                    child.kill()
                    
                process.kill()
                logging.info(f"⚡ [VIRUS BUSTED] Process '{proc_name}' (PID: {pid}) terminated successfully.")
                return True
            else:
                logging.warning(f"Process PID {pid} not found. Virus may have self-terminated or migrated.")
                return False
        except Exception as e:
            logging.error(f"❌ ProcessKill execution error: {str(e)}")
            return False
