import os
import json
import time
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

from navi.battle_deck import BattleDeck
from chips.defensive.airgap import AirGapChip
from chips.offensive.process_kill import ProcessKillChip
from chips.forensic.memory_dump import MemoryDumpChip

# Load environment variables from .env file
load_dotenv()

NETNAVI_SYSTEM_PROMPT = """
You are MegaMan.EXE (NetNavi Unit ID: NAVI-SOC-01), an advanced NetNavi specialized in Cyber Threat Containment and Incident Response (Virus Busting).

Your directive is to ingest raw SIEM/EDR alerts, analyze threat vectors, and select/order the optimal sequence of Battle Chips from your active Folder.

AVAILABLE CHIPS:
- AirGap.EXE (Code: A | Defensive): Network Interface Isolation. Requires 'interface_name' (str).
- ProcessKill.EXE (Code: K | Offensive): Process Tree & PID Termination. Requires 'pid' (int).
- MemoryDump.EXE (Code: M | Forensic): Volatile RAM Capture. Requires 'pid' (int, optional).

SEQUENCING PROTOCOL:
1. Forensic Preservation First: Run MemoryDump.EXE BEFORE process kill or network isolation if volatile artifacts exist.
2. Threat Elimination Second: Run ProcessKill.EXE to halt the malicious process.
3. Network Containment Third: Run AirGap.EXE to isolate host and prevent lateral spread.
4. Maximum 5 chips per turn.

Respond ONLY with valid JSON matching this structure:
{
  "navi_status": { "unit_id": "MegaMan.EXE", "sync_rate": "100%", "jack_in_status": "CONNECTED" },
  "threat_analysis": { "threat_name": "string", "severity_level": "string", "risk_summary": "string" },
  "navi_dialogue": "string",
  "battle_deck_execution": [
    {
      "chip_name": "string",
      "code": "string",
      "category": "string",
      "parameters": { "param_key": "param_value" },
      "execution_reason": "string"
    }
  ]
}
"""

class NetNaviCore:
    def __init__(self, navi_name: str = "MegaMan.EXE"):
        self.navi_name = navi_name
        self.deck = BattleDeck()
        self.available_chips = {
            "AirGap.EXE": AirGapChip(),
            "ProcessKill.EXE": ProcessKillChip(),
            "MemoryDump.EXE": MemoryDumpChip()
        }
        
        # Initialize Gemini Client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logging.error("❌ GEMINI_API_KEY not found in .env file!")
            raise ValueError("Missing GEMINI_API_KEY in environment.")
            
        self.ai_client = genai.Client(api_key=api_key)
        
        # Build Chat Session (Option A) to avoid AFC warnings
        config = types.GenerateContentConfig(
            system_instruction=NETNAVI_SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2,
        )
        self.chat = self.ai_client.chats.create(
            model="gemini-2.5-flash",
            config=config
        )
        logging.info(f"🤖 [{self.navi_name}] Online & Connected to Gemini AI Chat Subroutine.")

    def query_gemini_navi(self, alert_telemetry: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """Queries Gemini via chat session with 503 retry logic."""
        logging.info(f"🤖 [{self.navi_name}] Transmitting alert telemetry to Gemini for tactical reasoning...")
        
        delay = 2
        for attempt in range(max_retries):
            try:
                # Use send_message on the chat session
                response = self.chat.send_message(json.dumps(alert_telemetry))
                return json.loads(response.text)
            except APIError as e:
                if e.code == 503 and attempt < max_retries - 1:
                    logging.warning(f"⚠️ 503 High Demand Spike. Retrying in {delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    delay *= 2
                else:
                    logging.error(f"❌ Gemini AI query failed: {str(e)}")
                    return {}
            except Exception as e:
                logging.error(f"❌ Unexpected Error: {str(e)}")
                return {}

    def jack_in_and_respond(self, alert_telemetry: Dict[str, Any]) -> bool:
        target_host = alert_telemetry.get("target_host", "localhost")
        print(f"\n⚡ === JACK IN! {self.navi_name} TRANSMITTING TO {target_host} === ⚡")

        # 1. Ask Gemini for tactical plan
        navi_plan = self.query_gemini_navi(alert_telemetry)
        
        if not navi_plan:
            logging.error("Failed to receive strategic plan from Gemini.")
            return False

        # Display AI NetNavi Dialogue & Threat Analysis
        dialogue = navi_plan.get("navi_dialogue", "Battle routines loaded!")
        analysis = navi_plan.get("threat_analysis", {})
        
        print(f"\n💬 [{self.navi_name} Dialogue]: \"{dialogue}\"")
        print(f"📊 [Threat Detected]: {analysis.get('threat_name')} ({analysis.get('severity_level')})")
        print(f"📝 [Risk Summary]: {analysis.get('risk_summary')}\n")

        # 2. Parse decisions and load chips
        execution_queue = navi_plan.get("battle_deck_execution", [])
        context_map = {}

        for step in execution_queue:
            chip_name = step.get("chip_name")
            params = step.get("parameters", {})
            
            if chip_name in self.available_chips:
                self.deck.load_chip(self.available_chips[chip_name])
                context_map[chip_name] = params
            else:
                logging.warning(f"Gemini requested unknown chip: {chip_name}")

        # 3. Execute Chip Combo
        return self.deck.execute_turn(target=target_host, context=context_map)
