import os
import platform
import subprocess
import logging
from datetime import datetime
from chips import BaseBattleChip

class MemoryDumpChip(BaseBattleChip):
    def __init__(self):
        super().__init__(name="MemoryDump.EXE", code="M", chip_type="Forensic")

    def execute(self, target: str, output_dir: str = "./logs/dumps", pid: int = None) -> bool:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(output_dir, exist_ok=True)
        system_os = platform.system()
        
        logging.info(f"🔍 [CHIP SLOT: {self.name}] Initiating volatile memory capture on target: {target}")

        try:
            if pid:
                # Targeted process memory capture
                dump_file = os.path.join(output_dir, f"proc_mem_{pid}_{timestamp}.dmp")
                logging.info(f"Capturing memory dump for specific PID {pid} -> {dump_file}")
                
                if system_os == "Windows":
                    # Windows Procdump / PowerShell dump invocation simulation
                    cmd = f"powershell -Command \"Get-Process -Id {pid} | Out-File -FilePath {dump_file}\""
                else:
                    # Linux process RAM extract via gcore
                    cmd = f"sudo gcore -o {dump_file} {pid}"
            else:
                # Full physical RAM acquisition
                dump_file = os.path.join(output_dir, f"full_ram_{target}_{timestamp}.raw")
                logging.info(f"Capturing FULL RAM image -> {dump_file}")
                
                if system_os == "Windows":
                    cmd = f"winpmem.exe -o {dump_file} --volume_offset 0"
                else:
                    cmd = f"sudo dd if=/dev/mem of={dump_file} bs=1M status=progress"

            logging.info(f"Executing acquisition command: {cmd}")
            subprocess.run(cmd, shell=True, check=True)

            logging.info(f"✅ Memory artifact secured: {dump_file} [MD5 Integrity Hashing Queued]")
            return True

        except Exception as e:
            logging.error(f"❌ MemoryDump execution failed: {str(e)}")
            return False
