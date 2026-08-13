import os
import random
import time
import subprocess

# The components of the military train vulnerable to Slash Beast's rampage
TRAIN_COMPARTMENTS = ["car_01_engine", "car_02_cargo", "the_conductor_snort"]

def slash_beast_charge():
    print("=" * 60)
    print("⚠️  WARNING: MAVERICK SIGNATURE DETECTED IN THE AREA...")
    print("🦁 SLASH BEAST USES 'RUNAWAY CHARGE'!")
    print("=" * 60)
    time.sleep(2)
    
    # Randomly select a target container to destroy
    target = random.choice(TRAIN_COMPARTMENTS)
    print(f"💥 CLAW IMPACT! Slash Beast has ripped through: [{target}]")
    
    # Force kill the target container
    cmd = f"sudo docker stop {target}"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    
    print(f"🛑 System Status: {target} has been derailed and knocked OFFLINE.")
    print("=" * 60)

if __name__ == "__main__":
    slash_beast_charge()
