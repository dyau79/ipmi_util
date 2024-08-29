import argparse
import subprocess
import sys

def check_ipmitool():
    try:
        subprocess.run(["ipmitool", "-V"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def run_ipmi_command(ip, username, password, command):
    base_cmd = ["ipmitool", "-I", "lanplus", "-H", ip, "-U", username, "-P", password]
    full_cmd = base_cmd + command
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing IPMI command: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def power_cycle(ip, username, password):
    print("Power cycling the server...")
    run_ipmi_command(ip, username, password, ["power", "cycle"])
    print("Power cycle command sent successfully.")

def set_pxe_boot(ip, username, password):
    print("Setting PXE boot for next reboot...")
    run_ipmi_command(ip, username, password, ["chassis", "bootdev", "pxe"])
    print("PXE boot set successfully for the next reboot.")

def main():
    parser = argparse.ArgumentParser(description="IPMI Management Script")
    parser.add_argument("ip", help="IPMI IP address")
    parser.add_argument("action", choices=["power_cycle", "set_pxe"], help="Action to perform")
    parser.add_argument("-u", "--username", default="ADMIN", help="IPMI username (default: ADMIN)")
    parser.add_argument("-p", "--password", required=True, help="IPMI password")
    args = parser.parse_args()

    if not check_ipmitool():
        print("Error: ipmitool is not installed or not in the system PATH.")
        print("Please install ipmitool and try again.")
        sys.exit(1)

    if args.action == "power_cycle":
        power_cycle(args.ip, args.username, args.password)
    elif args.action == "set_pxe":
        set_pxe_boot(args.ip, args.username, args.password)

if __name__ == "__main__":
    main()
