import subprocess

def apply_block(ip, chain):
    try:
        subprocess.run(["sudo", "iptables", "-I", chain, "-s", ip, "-j", "DROP"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
