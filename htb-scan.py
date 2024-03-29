"""Module to scan an HTB machine, depends on the HTB-Admin package."""
import os
from argparse import ArgumentParser, Namespace


def udp_scan(outdir: str, target: str, ports: str) -> None:
    """Runs the udp scan against specified number of top ports"""

    command = f"nmap -sU --top-ports {ports} --open -v " \
              f"-oN {outdir}/udp_top_{ports}.nmap {target}"

    print(f"[*] Executing udp scan on top {ports} " \
           "ports with the following command...")
    print(command)
    os.system(command)


def enum_scan(outdir: str, target: str) -> None:
    """Runs the more comprehensive enum scan for nmap"""

    command = f"nmap -p- -sV -sC -v -oN {outdir}/enum_all.nmap " \
              f"--min-rate 4500 --max-rtt-timeout 1500ms {target}"

    print("[*] Executing enum scan with the following command...")
    print(command)
    os.system(command)


def nmap_scan(outdir: str, target: str) -> None:
    """Runs the full panel nmap scan against target host"""

    stealth_scan = f"nmap -sS -p- -oN {outdir}/open_ports.nmap {target}"
    port_string = f"ports=$(cat {outdir}/open_ports.nmap|grep ^[0-9]" \
                   "|cut -d '/' -f 1|tr '\\n' ','|sed s/,$//)"
    service_scan = f"nmap -sV -p $ports -oN " \
                   f"{outdir}/service_versions.nmap {target}"
    full_scan = f"nmap -A -p $ports -oN {outdir}/full_scan.nmap {target}"
    commands = [stealth_scan, port_string, service_scan, full_scan]
    command = ";".join(commands)

    print("[*] Executing the following compiled command...")
    print(command)
    os.system(command)


def adjust_permissions(outdir: str) -> None:
    """Adjust the permission for scan results to user's permission."""

    uid = os.environ.get("SUDO_UID", 0)
    gid = os.environ.get("SUDO_UID", 0)
 
    os.system(f"chown -R {uid}:{gid} {outdir}")


def execute_scan(outdir: str,
                 target: str,
                 args: Namespace
                 ) -> None:
    """Execute the corresponding Nmap scan based on cmdline paramaters."""

    if args.enum is True:
        enum_scan(outdir, target)
    elif args.udp is not None:
        udp_scan(outdir, target, args.udp)
    else:
        nmap_scan(outdir, target)

    adjust_permissions(outdir)


def main(args: Namespace) -> None:
    target = args.target
    outdir = args.outdir.rstrip("/")

    print(f"[*] Running nmap scan on (target: {target}) " \
          f"and writing results to (directory: {outdir}).")

    if not os.path.isdir(outdir):
        print(f"[!] Directory (path: {outdir}) " \
               "does not exist, creating it now.")
        os.makedirs(outdir)

    execute_scan(outdir, target, args)

    print("[!] Finished running nmap scans.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-t", "--target",
        default="`htb-admin -t`",
        help="specify target host"
    )
    parser.add_argument(
        "-o", "--outdir",
        default="nmap",
        help="specify output directory"
    )
    parser.add_argument(
        "-e", "--enum",
        action="store_true",
        help="specify enum scan flag"
    )
    parser.add_argument(
        "-u", "--udp",
        required=False, type=int, nargs='?', const=100,
        help="specify udp flag with number of top ports to scan"
    )
    args = parser.parse_args()

    if not os.getuid():
        main(args)
    else:
        raise PermissionError("Must be run as root!")
