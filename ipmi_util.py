import argparse
import subprocess

def run_ipmi_command(ip_address, command):
    full_command = f"ipmitool -I lanplus -H {ip_address} -U <username> -P <password> {command}"
    try:
        result = subprocess.run(full_command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing IPMI command: {e}")
        return None

def power_cycle(ip_address):
    print(f"Power cycling server at {ip_address}")
    result = run_ipmi_command(ip_address, "power cycle")
    if result:
        print("Power cycle command sent successfully")
    else:
        print("Failed to send power cycle command")

def set_pxe_boot(ip_address):
    print(f"Setting PXE boot for next reboot on server at {ip_address}")
    # Set boot device to PXE
    result1 = run_ipmi_command(ip_address, "chassis bootdev pxe")
    # Ensure the PXE boot is set for the next boot only
    result2 = run_ipmi_command(ip_address, "chassis bootdev pxe options=persistent")
    
    if result1 and result2:
        print("PXE boot set successfully for next reboot")
    else:
        print("Failed to set PXE boot")

def main():
    parser = argparse.ArgumentParser(description="IPMI Control Script")
    parser.add_argument("ip_address", help="IPMI IP address of the server")
    parser.add_argument("action", choices=["power_cycle", "set_pxe"], help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "power_cycle":
        power_cycle(args.ip_address)
    elif args.action == "set_pxe":
        set_pxe_boot(args.ip_address)

if __name__ == "__main__":
    main()
